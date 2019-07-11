#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jip import commands, logger
from jip.maven import Artifact
from typing import List
from . import API
from .jvm import koala_class_of, string, java_list, is_jvm_running, start_jvm, check_jvm, shutdown_jvm
from .types import *
from pathlib import Path

# ------- Repository Setup --------

# Local Maven repo
commands.repos_manager.add_repos('local-maven',
                                 str(Path(Path.home(), ".m2", "repository").absolute()), 'local',
                                 order=0)
# Local Ivy2 repo
commands.repos_manager.add_repos('local-ivy2',
                                 str(Path(Path.home(), ".ivy2", "cache").absolute()), 'local',
                                 order=1)
# Sonatype repo
commands.repos_manager.add_repos('sonatype',
                                 'https://oss.sonatype.org/content/repositories/public/', 'remote',
                                 order=2)
# JCenter
commands.repos_manager.add_repos('jcenter', 'http://jcenter.bintray.com/', 'remote', order=3)

# Jitpack for Komoran v3
commands.repos_manager.add_repos('jitpack.io', 'https://jitpack.io/', 'remote', order=4)

# Maven Central & its mirror
commands.repos_manager.add_repos('central1', 'http://repo1.maven.org/maven2/', 'remote',
                                 order=5)
commands.repos_manager.add_repos('central2', 'http://central.maven.org/maven2/', 'remote',
                                 order=6)


def _retrieve_latest_version(group, artifact) -> str:
    import requests
    import re

    url = 'https://oss.sonatype.org/content/repositories/public/%s/%s' % (group.replace('.', '/'), artifact)
    result = requests.get(url).text
    result = [line.split('/')[-1] for line in re.findall('%s/(\d+\.\d+\.\d+)/' % url, result)]
    version = max(result)

    logger.info('[INFO] Latest version of %s:%s (%s) will be used.', group, artifact, version)
    return version


class _ArtifactClsf(Artifact):
    def to_maven_name(self, ext):
        if self.classifier is None or ext == "pom":
            return super().to_maven_name(ext)
        else:
            group = self.group.replace('.', '/')
            return "%s/%s/%s/%s-%s-%s.%s" % (group, self.artifact, self.version, self.artifact,
                                             self.version, self.classifier, ext)

    def to_maven_snapshot_name(self, ext):
        if self.classifier is None or ext == "pom":
            return super().to_maven_snapshot_name(ext)
        else:
            group = self.group.replace('.', '/')
            version_wo_snapshot = self.version.replace('-SNAPSHOT', '')
            return "%s/%s/%s/%s-%s-%s-%s-%s.%s" % (group, self.artifact, self.version, self.artifact,
                                                   version_wo_snapshot,
                                                   self.timestamp, self.build_number, self.classifier, ext)

    def __init__(self, group, artifact, version=None, classifier=None):
        if version is None or version.upper() == "LATEST":
            version = _retrieve_latest_version(group, artifact)
        super().__init__(group, artifact, version)
        self.classifier = classifier


# JIP 코드 참조하여 변경함.
def _find_pom(artifact):
    """ find pom and repos contains pom """
    # lookup cache first
    if commands.cache_manager.is_artifact_in_cache(artifact):
        pom = commands.cache_manager.get_artifact_pom(artifact)
        return pom, commands.cache_manager.as_repos()
    else:
        for repos in commands.repos_manager.repos:
            pom = repos.download_pom(artifact)
            # find the artifact
            if pom is not None:
                commands.cache_manager.put_artifact_pom(artifact, pom)
                return pom, repos
        return None


# JIP 코드 참조하여 변경함.
def _resolve_artifacts_modified(artifacts, exclusions=[]):
    # download queue
    download_list = []

    # dependency_set contains artifact objects to resolve
    dependency_stack = set()

    for a in artifacts:
        dependency_stack.add(a)

    while len(dependency_stack) > 0:
        artifact = dependency_stack.pop()

        if commands.index_manager.is_same_installed(artifact) and artifact not in download_list:
            continue

        if any(map(artifact.is_same_artifact, exclusions)):
            continue

        pominfo = _find_pom(artifact)
        if pominfo is None:
            if not any(map(artifact.is_same_artifact, exclusions)):
                commands.logger.warning("[Warning] Artifact is not found: %s", artifact)
            # Ignore this unknown pom.
            continue

        if not commands.index_manager.is_installed(artifact):
            pom, repos = pominfo

            # repos.download_jar(artifact, get_lib_path())
            artifact.repos = repos

            if not any(map(artifact.is_same_artifact, exclusions)):
                download_list.append(artifact)
                commands.index_manager.add_artifact(artifact)

            pom_obj = commands.Pom(pom)
            for r in pom_obj.get_repositories():
                commands.repos_manager.add_repos(*r)

            more_dependencies = pom_obj.get_dependencies()
            for d in more_dependencies:
                d.exclusions.extend(artifact.exclusions)
                if not commands.index_manager.is_same_installed(d):
                    dependency_stack.add(d)

    return download_list


def initialize(java_options="-Xmx4g -Dfile.encoding=utf-8", **packages):
    """
    초기화 함수. 필요한 Java library를 다운받습니다.
    한번 초기화 된 다음에는 :py:func:`koalanlp.Util.finalize` 을 사용해 종료하지 않으면 다시 초기화 할 수 없습니다.

    :param str java_options: 자바 JVM option (기본값: "-Xmx4g -Dfile.encoding=utf-8")
    :param Dict[str,str] packages: 사용할 분석기 API의 목록. (Keyword arguments; 기본값: KMR="LATEST")
    :raise Exception: JVM이 2회 이상 초기화 될때 Exception.
    """

    if len(packages) == 0:
        packages = {
            API.KMR: "LATEST"
        }
        commands.logger.info("[Warning] Since no package names are specified, I'll load packages by default: %s" %
                             str(packages))

    if not is_jvm_running():
        java_options = java_options.split(" ")
        packages = {getattr(API, k.upper()): v for k, v in packages.items()}

        deps = [_ArtifactClsf('kr.bydelta', 'koalanlp-%s' % pack, version,
                              'assembly' if pack in API._REQUIRE_ASSEMBLY_ else None)
                for pack, version in packages.items()]
        # Add py4j jar
        deps.append(_ArtifactClsf('net.sf.py4j', 'py4j', '0.10.8.1'))

        exclusions = [_ArtifactClsf('com.jsuereth', 'sbt-pgp', '*')]

        down_list = _resolve_artifacts_modified(deps, exclusions=exclusions)
        down_list.sort(key=lambda a: a.repos.uri)

        for artifact in down_list:
            local_path = commands.cache_manager.get_jar_path(artifact)
            if artifact.repos != commands.cache_manager.as_repos():
                artifact.repos.download_jar(artifact, local_path)

        classpaths = [commands.cache_manager.get_jar_path(artifact, filepath=True)
                      for artifact in down_list]
        commands.pool.join()
        start_jvm(java_options, classpaths)

        try:
            check_jvm()
        except Exception as e:
            raise Exception("JVM test failed because %s" % str(e))

        # Enum 항목 초기화
        POS.values()
        PhraseTag.values()
        DependencyTag.values()
        RoleType.values()
        CoarseEntityType.values()

        commands.logger.info("JVM initialization procedure is completed.")
    else:
        raise Exception("JVM cannot be initialized more than once."
                        "Please call koalanlp.Util.done() when you want to re-initialize the JVM with other options.")


def finalize():
    """
    사용이 종료된 다음, 실행되어 있는 JVM을 종료합니다.
    """
    if is_jvm_running():
        shutdown_jvm()


def contains(string_list: List[str], tag) -> bool:
    """
    주어진 문자열 리스트에 구문분석 표지자/의존구문 표지자/의미역 표지/개체명 분류가 포함되는지 확인합니다.

    :param List[str] string_list: 분류가 포함되는지 확인할 문자열 목록
    :param Union[PhraseTag,DependencyTag,CoarseEntityType,RoleType] tag: 포함되는지 확인할 구문분석 표지자/의존구문 표지자/의미역 표지/개체명 분류
    :rtype: bool
    :return: 포함되면 true
    """

    if type(tag) is PhraseTag or type(tag) is DependencyTag or type(tag) is CoarseEntityType or type(tag) is RoleType:
        return koala_class_of('Util').contains(java_list([string(s) for s in string_list]) ,tag.reference)
    else:
        return False


# -------- Declare members exported ---------

__all__ = ['initialize', 'contains', 'finalize']

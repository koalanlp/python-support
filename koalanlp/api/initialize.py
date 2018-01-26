#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jip import commands
from jip.maven import Artifact
from .const import API, _artifactName
from typing import List
import os


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

        pominfo = _find_pom(artifact)
        if pominfo is None:
            if not any(map(artifact.is_same_artifact, exclusions)):
                commands.logger.warn("[Warning] Artifact is not found: %s", artifact)
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


not_assembly = [API.EUNJEON, API.KOMORAN, API.TWITTER]


def initialize(packages=[API.EUNJEON, API.KKMA],
               version="1.9.2",
               java_options="-Xmx4g -Dfile.encoding=utf-8"):
    """
    초기화 함수. 필요한 Java library를 다운받습니다.

    :param List[API] packages: 사용할 분석기 API의 목록. (기본값: [API.EUNJEON, API.KKMA])
    :param str version: 사용할 분석기의 버전. (기본값: "1.9.2")
    :param str java_options: 자바 JVM option (기본값: "-Xmx4g -Dfile.encoding=utf-8")
    :raise Exception: JVM이 2회 이상 초기화 될때 Exception.
    """
    import jnius_config
    from pathlib import Path
    global not_assembly
    if not jnius_config.vm_running:
        java_options = java_options.split(" ")
        jnius_config.add_options(*java_options)

        deps = [_ArtifactClsf('kr.bydelta', 'koalanlp-%s_2.12' % _artifactName(pack), version,
                              None if pack in not_assembly else "assembly") for pack in packages]
        exclusions = [_ArtifactClsf('com.jsuereth', 'sbt-pgp', '*')]

        # Local Maven repo
        commands.repos_manager.add_repos('local-maven',
                                         os.path.join(str(Path.home()), ".m2", "repository"), 'local',
                                         order=0)
        # Local Ivy2 repo
        commands.repos_manager.add_repos('local-ivy2',
                                         os.path.join(str(Path.home()), ".ivy2", "cache"), 'local',
                                         order=1)
        # Sonatype repo
        commands.repos_manager.add_repos('sonatype',
                                         'https://oss.sonatype.org/content/repositories/public/', 'remote',
                                         order=2)
        # Maven Central & its mirror
        commands.repos_manager.add_repos('central1', 'http://repo1.maven.org/maven2/', 'remote',
                                         order=3)
        commands.repos_manager.add_repos('central2', 'http://central.maven.org/maven2/', 'remote',
                                         order=4)
        # Jitpack for Komoran v3
        commands.repos_manager.add_repos('jitpack.io', 'https://jitpack.io/', 'remote',
                                         order=5)

        down_list = _resolve_artifacts_modified(deps, exclusions=exclusions)
        down_list.sort(key=lambda a: a.repos.uri)

        for artifact in down_list:
            local_path = commands.cache_manager.get_jar_path(artifact)
            if artifact.repos != commands.cache_manager.as_repos():
                artifact.repos.download_jar(artifact, local_path)

        classpaths = [commands.cache_manager.get_jar_path(artifact, filepath=True)
                      for artifact in down_list]
        commands.pool.join()
        jnius_config.add_classpath(*classpaths)

        try:
            # Test jvm
            from jnius import autoclass
            JString = autoclass("java.lang.String")
            JString("")
        except:
            raise Exception("JVM cannot be initialized. I think JVM has been initialized by other packages already. Please check!")

        commands.logger.info("JVM initialization procedure is completed.")
    else:
        raise Exception("JVM cannot be initialized. I think JVM has been initialized by other packages already. Please check!")

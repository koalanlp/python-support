#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import shutil

from pathlib import Path
from typing import List

from . import API
from .jvm import koala_class_of, string, java_list, is_jvm_running, start_jvm, check_jvm, shutdown_jvm
from .types import *

from koalanlp.jip.repository import RepositoryManager
from koalanlp.jip.index import IndexManager
from koalanlp.jip.cache import CacheManager
from koalanlp.jip.maven import Artifact, Pom
from koalanlp.jip.util import wait_until_download_finished

# Logging setup
logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("py4j").setLevel(logging.WARNING)
logger = logging.getLogger('koalanlp.jip')

# ------- Repository Setup --------
repos_manager = RepositoryManager()
index_manager = None
cache_manager = None

# Local Ivy2 repo
repos_manager.add_repos('local-ivy2', str(Path(Path.home(), ".ivy2", "cache").absolute()), 'local', order=1)
# Sonatype repo
repos_manager.add_repos('sonatype',
                        'https://oss.sonatype.org/content/repositories/public/', 'remote', order=2)
# JCenter
repos_manager.add_repos('jcenter', 'https://jcenter.bintray.com/', 'remote', order=3)

# Jitpack for Komoran v3
repos_manager.add_repos('jitpack.io', 'https://jitpack.io/', 'remote', order=4)

# Maven Central
repos_manager.add_repos('central1', 'https://repo1.maven.org/maven2/', 'remote', order=5)
repos_manager.add_repos('central2', 'http://insecure.repo1.maven.org/maven2/', 'remote', order=6)


# JIP 코드 참조하여 변경함.
def _find_pom(artifact):
    """ find pom and repos contains pom """
    # lookup cache first
    if cache_manager.is_artifact_in_cache(artifact):
        pom = cache_manager.get_artifact_pom(artifact)
        return pom, cache_manager.as_repos()
    else:
        for repos in repos_manager.repos:
            pom = repos.download_pom(artifact)
            # find the artifact
            if pom is not None:
                cache_manager.put_artifact_pom(artifact, pom)
                return pom, repos
        return None


# JIP 코드 참조하여 변경함.
def _resolve_artifacts_modified(artifacts, exclusions=None):
    global index_manager, cache_manager, repos_manager

    if exclusions is None:
        exclusions = []

    # download queue
    download_list = []

    # dependency_set contains artifact objects to resolve
    dependency_stack = set()

    for a in artifacts:
        dependency_stack.add(a)

    while len(dependency_stack) > 0:
        artifact = dependency_stack.pop()

        if index_manager.is_same_installed(artifact) and artifact not in download_list:
            continue

        if any(map(artifact.is_same_artifact, exclusions)):
            continue

        pominfo = _find_pom(artifact)
        if pominfo is None:
            if not any(artifact.is_same_artifact(a) for a in exclusions):
                logger.warning("[Warning] Artifact is not found: %s", artifact)
            # Ignore this unknown pom.
            continue

        if not index_manager.is_installed(artifact):
            pom, repos = pominfo

            # repos.download_jar(artifact, get_lib_path())
            artifact.repos = repos

            if not any(map(artifact.is_same_artifact, exclusions)):
                download_list.append(artifact)
                index_manager.add_artifact(artifact)

            pom_obj = Pom(pom, repos_manager, cache_manager)
            for r in pom_obj.get_repositories():
                repos_manager.add_repos(*r)

            more_dependencies = pom_obj.get_dependencies()
            for d in more_dependencies:
                d.exclusions.extend(artifact.exclusions)
                if not index_manager.is_same_installed(d):
                    dependency_stack.add(d)

    return download_list


def initialize(java_options="-Xmx1g -Dfile.encoding=utf-8", lib_path=None, force_download=False, **packages):
    """
    초기화 함수. 필요한 Java library를 다운받습니다.
    한번 초기화 된 다음에는 :py:func:`koalanlp.Util.finalize` 을 사용해 종료하지 않으면 다시 초기화 할 수 없습니다.

    :param str java_options: 자바 JVM option (기본값: "-Xmx1g -Dfile.encoding=utf-8")
    :param Optional[str] lib_path: 자바 라이브러리를 저장할 '.java' 디렉터리/폴더가 위치할 곳. (기본값: None = os.cwd())
    :param bool force_download: 자바 라이브러리를 모두 다 다시 다운로드할 지의 여부. (기본값: False)
    :param Dict[str,str] packages: 사용할 분석기 API의 목록. (Keyword arguments; 기본값: KMR="LATEST")
    :raise Exception: JVM이 2회 이상 초기화 될때 Exception.
    """
    if len(packages) == 0:
        packages = {
            API.KMR: "LATEST"
        }
        logger.info("[Warning] Since no package names are specified, I'll load packages by default: %s" %
                     str(packages))

    if not lib_path:
        lib_path = Path.cwd()

    if force_download:
        clear_all_downloaded_jars(lib_path)

    # Initialize cache & index manager
    global cache_manager, index_manager
    cache_manager = CacheManager(lib_path)
    index_manager = IndexManager(lib_path)

    if not is_jvm_running():
        java_options = java_options.split(" ")
        packages = {getattr(API, k.upper()): v for k, v in packages.items()}

        deps = [Artifact('kr.bydelta', 'koalanlp-%s' % pack, version,
                         'assembly' if pack in API._REQUIRE_ASSEMBLY_ else None)
                for pack, version in packages.items()]
        # Add py4j jar
        deps.append(Artifact('net.sf.py4j', 'py4j', '0.10.8.1'))

        exclusions = [Artifact('com.jsuereth', 'sbt-pgp', '*')]

        down_list = _resolve_artifacts_modified(deps, exclusions=exclusions)
        down_list.sort(key=lambda a: a.repos.uri)

        for artifact in down_list:
            local_path = cache_manager.get_jar_path(artifact)
            if artifact.repos != cache_manager.as_repos():
                artifact.repos.download_jar(artifact, local_path)

        # Get all installed JAR files
        classpaths = [cache_manager.get_jar_path(artifact, filepath=True)
                      for artifact in index_manager.installed]
        wait_until_download_finished()
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

        logger.info("JVM initialization procedure is completed.")
    else:
        raise Exception("JVM cannot be initialized more than once."
                        "Please call koalanlp.Util.finalize() when you want to re-init the JVM with other options.")


def finalize():
    """
    사용이 종료된 다음, 실행되어 있는 JVM을 종료합니다.
    :return: 실행 이후 JVM이 꺼져있다면 True.
    """
    if is_jvm_running():
        is_running = shutdown_jvm()
        return not is_running
    else:
        return True


def clear_all_downloaded_jars(lib_path=None):
    """
    다운로드 된 자바 라이브러리를 삭제합니다.
    :param Optional[str] lib_path: 자바 라이브러리를 저장할 '.java' 디렉터리/폴더가 위치한 곳. (Default: None, i.e. os.cwd())
    """
    if not lib_path:
        lib_path = Path.cwd()

    java_path = Path(lib_path, '.java')
    if java_path.exists():
        shutil.rmtree(java_path)


def contains(string_list: List[str], tag) -> bool:
    """
    주어진 문자열 리스트에 구문분석 표지자/의존구문 표지자/의미역 표지/개체명 분류가 포함되는지 확인합니다.

    :param List[str] string_list: 분류가 포함되는지 확인할 문자열 목록
    :param Union[PhraseTag,DependencyTag,CoarseEntityType,RoleType] tag: 포함되는지 확인할 구문분석 표지자/의존구문 표지자/의미역 표지/개체명 분류
    :rtype: bool
    :return: 포함되면 true
    """

    if type(tag) is PhraseTag or type(tag) is DependencyTag or type(tag) is CoarseEntityType or type(tag) is RoleType:
        return koala_class_of('Util').contains(java_list([string(s) for s in string_list]), tag.reference)
    else:
        return False


# -------- Declare members exported ---------

__all__ = ['initialize', 'contains', 'finalize', 'clear_all_downloaded_jars']

import shutil
import invoke
import pathlib
import commandscript


def get_cache_dir(debug: bool) -> str:
    build_type = "Debug" if debug else "Release"
    return f"{commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.exp}/.cache_Conan_{build_type}"


def get_build_dir(debug: bool, project_name: str) -> str:
    build_type = "Debug" if debug else "Release"
    return f"{commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.exp}/.build_Conan_for_{project_name}_{build_type}"


def get_toolchain_file_path(debug: bool, project_name: str):
    build_type = "Debug" if debug else "Release"
    return f"{get_build_dir(debug, project_name)}/build/{build_type}/generators/conan_toolchain.cmake"


@commandscript.script_task()
def clean(_ctx):
    """
    Clean Conan's data.
    """
    artifacts_dir = pathlib.Path(commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.exp)
    if artifacts_dir.exists() == False:
        return

    for item in artifacts_dir.iterdir():
        item = artifacts_dir / item
        if item.is_dir():
            if item.name.startswith('.cache_Conan'):
                shutil.rmtree(item)
                commandscript.info.log_line(f"remove conan cache dir: {item}")
            elif item.name.startswith('.build_Conan'):
                shutil.rmtree(item)
                commandscript.info.log_line(f"remove conan build dir: {item}")


@commandscript.script_task(
    help={
        "conanfile_dir": "path to target conanfile.txt",
        "project-name": "name project of conan's utilities consuming",
        "debug": "if set configuration type will be DEBUG (else RELEASE)",
    })
def install(ctx, conanfile_dir: str, project_name: str = None, debug=True):
    """
    Install dependencies via Conan.
    """
    assert project_name
    build_type = "Debug" if debug else "Release"
    return commandscript.ScriptExecutor.from_ctx(ctx)\
        .add_cwd(conanfile_dir)\
        .add_command([
            f'conan install .',
            f'--profile "{commandscript.ENV_CONTEXT.PROJECT_GIT_DIR.name}/conanprofile.txt"',
            f'--build=missing',
            f'--settings=build_type={build_type}',
            f'--settings=compiler.runtime_type={build_type}',
            f'--conf tools.cmake.cmaketoolchain:user_presets=False',
            f'--core-conf=core.download:parallel=8',
            f'--core-conf=core.cache:storage_path="{get_cache_dir(build_type)}"',
            f'--output-folder="{get_build_dir(build_type, project_name)}"',
        ])\
        .execute(f"{project_name}.conan.install.log")


collection = invoke.Collection("conan")
collection.add_task(clean, name="clean")
collection.add_task(install, name="install")

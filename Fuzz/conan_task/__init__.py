import shutil
import invoke
import pathlib
import commandscript


def get_build_dir(debug=True):
    build_type = "Debug" if debug else "Release"
    return f"{commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.exp}/.build_Conan_{build_type}"


def get_cache_dir(debug=True):
    build_type = "Debug" if debug else "Release"
    return f"{commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.exp}/.cache_Conan_{build_type}"


def get_toolchain_file_path(debug=True):
    build_type = "Debug" if debug else "Release"
    return f"{get_build_dir(debug)}/build/{build_type}/generators/conan_toolchain.cmake"


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
                commandscript.INFO.log_line(f"remove conan cache dir: {item}")
            elif item.name.startswith('.build_Conan'):
                shutil.rmtree(item)
                commandscript.INFO.log_line(f"remove conan build dir: {item}")


@commandscript.script_task(help={
    "profile_path": "path to target Conan profile file",
    "debug": "if set configuration type will be DEBUG (else RELEASE)",
})
def install(ctx, profile_path: str, debug=True):
    """
    Install dependencies via Conan.
    """
    build_type = "Debug" if debug else "Release"
    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(profile_path)\
        .add_command([
            f'conan install .',
            f'--profile conanprofile.txt',
            f'--build=missing',
            f'--settings=build_type={build_type}',
            f'--settings=compiler.runtime_type={build_type}',
            f'--core-conf=core.download:parallel=8',
            f'--core-conf=core.cache:storage_path="{get_cache_dir(build_type)}"',
            f'--output-folder="{get_build_dir(build_type)}"',
        ])\
        .execute("conan.install.log")


collection = invoke.Collection("conan")
collection.add_task(clean, name="clean")
collection.add_task(install, name="install")

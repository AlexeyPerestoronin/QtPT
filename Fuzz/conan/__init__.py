import shutil
import invoke
import pathlib
import commandscript


@commandscript.script_task()
def clean(_ctx):
    """
    Clean Conan's data.
    """
    conan_dir = pathlib.Path(commandscript.ENV_CONTEXT.PROJECT_CONAN_DIR.exp)
    if conan_dir.exists() == False:
        return

    for item in conan_dir.iterdir():
        item = conan_dir / item
        if item.is_dir():
            if item.name.startswith('.cache'):
                shutil.rmtree(item)
                commandscript.INFO.log_line(f"remove conan cache dir: {item}")
            elif item.name.startswith('.build'):
                shutil.rmtree(item)
                commandscript.INFO.log_line(f"remove conan build dir: {item}")


@commandscript.script_task(help={
    "debug":
    "if set configuration type will be DEBUG (else RELEASE)",
}, )
def install(ctx, debug=True):
    """
    Install dependencies via Conan.
    """

    build_type = "Debug" if debug else "Release"
    conan_dir = commandscript.ENV_CONTEXT.PROJECT_CONAN_DIR.name

    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(conan_dir)\
        .add_command([
            f'conan install .',
            f'--profile conanprofile.txt',
            f'--build=missing',
            f'--settings=build_type={build_type}',
            f'--settings=compiler.runtime_type={build_type}',
            f'--core-conf=core.cache:storage_path="{conan_dir}/.cache_{build_type}"',
            f'--core-conf=core.download:parallel=8',
            f'--output-folder="{conan_dir}/.build_{build_type}"',
        ])\
        .execute("leet_code-conan.install.log")


collection = invoke.Collection("conan")
collection.add_task(clean, name="clean")
collection.add_task(install, name="install")

import shutil
import invoke
import pathlib
import commandscript


@commandscript.script_task(help={
    "src": "conan source directory",
})
def clean(ctx, src: str):
    """
    Clean Conan's data.
    """
    src = pathlib.Path(src)
    if src.exists() == False:
        return

    for item in src.iterdir():
        item = src / item
        if item.is_dir():
            if item.name.startswith('.cache'):
                shutil.rmtree(item)
                commandscript.INFO.log_line(f"remove conan cache dir: {item}")
            elif item.name.startswith('.build'):
                shutil.rmtree(item)
                commandscript.INFO.log_line(f"remove conan build dir: {item}")


@commandscript.script_task(help={
    "src": "conan source directory",
    "debug": "if set configuration type will be DEBUG (else RELEASE)",
})
def install(ctx, src: str, debug=True):
    """
    Install dependencies via Conan.
    """
    build_type = "Debug" if debug else "Release"
    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(src)\
        .add_command([
            f'conan install .',
            f'--profile conanprofile.txt',
            f'--build=missing',
            f'--settings=build_type={build_type}',
            f'--settings=compiler.runtime_type={build_type}',
            f'--core-conf=core.cache:storage_path="{src}/.cache_{build_type}"',
            f'--core-conf=core.download:parallel=8',
            f'--output-folder="{src}/.build_{build_type}"',
        ])\
        .execute("conan.install.log")


collection = invoke.Collection("conan")
collection.add_task(clean, name="clean")
collection.add_task(install, name="install")

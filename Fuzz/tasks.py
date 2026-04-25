import pathlib
import invoke
import commandscript


commandscript.ENV_CONTEXT\
    .add_env_var('PROJECT_GIT_DIR', str(pathlib.Path(f'{__file__}').parent.parent))\
    .add_env_var('PROJECT_FUZZ_DIR', '${PROJECT_GIT_DIR}/Fuzz')\
    .add_env_var('COMMANDSCRIPT_SCRIPT_DIR', '${PROJECT_FUZZ_DIR}/.generated')\
    .add_env_var('PROJECT_ARTIFACTS_DIR', '${PROJECT_GIT_DIR}/.artifacts')\
    .add_env_var('USER_INPUT_HISTORY_DIR', '${PROJECT_GIT_DIR}/UserInputHistory')


@commandscript.script_task()
def get_info(ctx):
    """
    Print to console information about active configuration of commandcript-tasks
    """
    names = [value.name for value in commandscript.ENV_CONTEXT.values()]
    hold_values = [value.hld for value in commandscript.ENV_CONTEXT.values()]
    expanded_values = [value.exp for value in commandscript.ENV_CONTEXT.values()]
    width = max(max(len(key) for key in names), max(len(item) for item in hold_values), max(len(item) for item in expanded_values), 25)
    commandscript.info.log_line("Active environment configuration:")
    commandscript.info.log_line(f"| {'Env-var name':<{width}} | {'Env-var hold-value':<{width}} | {'Env-var expanded-value':<{width}} |")
    commandscript.info.log_line(f"|-{'-' * width}-|-{'-' * width}-|-{'-' * width}-|")
    for i in range(len(names)):
        key = names[i]
        hold_value = hold_values[i]
        expanded_value = expanded_values[i]
        if expanded_value == hold_value:
            expanded_value = '-'
        commandscript.info.log_line(f"| {key:<{width}} | {hold_value:<{width}} | {expanded_value:<{width}} |")


@commandscript.script_task()
def yapf(ctx):
    """
    Format python files in Fuzz
    """
    commandscript.ScriptExecutor.from_ctx(ctx)\
        .add_cwd(commandscript.ENV_CONTEXT.PROJECT_FUZZ_DIR)\
        .add_command([
                'yapf',
                f'--style "{commandscript.ENV_CONTEXT.PROJECT_GIT_DIR}/.style.yapf"',
                '--verbose',
                '--recursive',
                '--in-place',
                '--parallel',
                f"--exclude '**.venv**'",
                f"{commandscript.ENV_CONTEXT.PROJECT_FUZZ_DIR}",
            ])\
        .execute(log="yapf.log")


namespace = invoke.Collection()
namespace.add_task(get_info, name="get-info")
namespace.add_task(yapf, name="yapf")

import conan_task

namespace.add_collection(conan_task.collection, name="conan")

import user_input_history

namespace.add_collection(user_input_history.collection, name="uih")

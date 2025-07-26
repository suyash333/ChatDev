import html
import logging
import re
import time

import markdown
import inspect
from camel.messages.system_messages import SystemMessage
from online_log.app import send_msg


def now():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def log_and_print_online(role, content=None):
    """
    Log and print messages with optional online sending.
    
    Args:
        role: The role/actor sending the message
        content: The message content (optional)
    """
    try:
        if not content:
            logging.info(role + "\n")
            try:
                send_msg("System", role)
            except Exception as e:
                logging.warning(f"Failed to send online message: {e}")
            print(role + "\n")
        else:
            print(str(role) + ": " + str(content) + "\n")
            logging.info(str(role) + ": " + str(content) + "\n")
            if isinstance(content, SystemMessage):
                try:
                    records_kv = []
                    content.meta_dict["content"] = content.content
                    for key in content.meta_dict:
                        value = content.meta_dict[key]
                        value = str(value)
                        value = html.unescape(value)
                        value = markdown.markdown(value)
                        value = re.sub(r'<[^>]*>', '', value)
                        value = value.replace("\n", " ")
                        records_kv.append([key, value])
                    content = "**[SystemMessage**]\n\n" + convert_to_markdown_table(records_kv)
                except Exception as e:
                    logging.warning(f"Failed to process SystemMessage: {e}")
                    content = str(content)
            else:
                role = str(role)
                content = str(content)
            try:
                send_msg(role, content)
            except Exception as e:
                logging.warning(f"Failed to send online message: {e}")
    except Exception as e:
        # Fallback to basic logging if everything fails
        print(f"Logging error: {e}")
        print(f"{role}: {content}")


def convert_to_markdown_table(records_kv):
    """
    Convert key-value pairs to a markdown table.
    
    Args:
        records_kv: List of [key, value] pairs
        
    Returns:
        str: Formatted markdown table
    """
    if not records_kv:
        return "| Parameter | Value |\n| --- | --- |\n| (none) | (none) |"
    
    # Create the Markdown table header
    header = "| Parameter | Value |\n| --- | --- |"

    # Create the Markdown table rows with proper escaping
    rows = []
    for key, value in records_kv:
        # Escape pipe characters that could break the table
        escaped_key = str(key).replace("|", "\\|")
        escaped_value = str(value).replace("|", "\\|")
        rows.append(f"| **{escaped_key}** | {escaped_value} |")

    # Combine the header and rows to form the final Markdown table
    markdown_table = header + "\n" + '\n'.join(rows)

    return markdown_table


def log_arguments(func):
    """
    Decorator to log function arguments in a formatted way.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function with argument logging
    """
    def wrapper(*args, **kwargs):
        try:
            sig = inspect.signature(func)
            params = sig.parameters

            all_args = {}
            all_args.update({name: value for name, value in zip(params.keys(), args)})
            all_args.update(kwargs)

            records_kv = []
            for name, value in all_args.items():
                if name in ["self", "chat_env", "task_type"]:
                    continue
                try:
                    value_str = str(value)
                    value_str = html.unescape(value_str)
                    value_str = markdown.markdown(value_str)
                    value_str = re.sub(r'<[^>]*>', '', value_str)
                    value_str = value_str.replace("\n", " ")
                    # Truncate very long values
                    if len(value_str) > 200:
                        value_str = value_str[:197] + "..."
                    records_kv.append([name, value_str])
                except Exception as e:
                    records_kv.append([name, f"<Error processing value: {e}>"])
                    
            records = f"**[{func.__name__}]**\n\n" + convert_to_markdown_table(records_kv)
            log_and_print_online("System", records)
        except Exception as e:
            # If logging fails, continue with function execution
            logging.warning(f"Failed to log arguments for {func.__name__}: {e}")

        return func(*args, **kwargs)

    return wrapper

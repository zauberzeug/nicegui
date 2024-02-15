from typing import Any, Dict, Optional

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish

from nicegui import ui


class NiceGuiLogElementCallbackHandler(BaseCallbackHandler):
    """Callback Handler that writes to a log element.

    This callback handler is designed to write log messages to a log element in a NiceGUI application.
    It provides methods to handle various events during the execution of a chain, agent actions, and agent finish.

    Usage:
    1. Create an instance of NiceGuiLogElementCallbackHandler, passing the log element as a parameter.
    2. Register the instance as a callback handler in your NiceGUI application.
    3. The log messages will be automatically written to the log element during the execution.

    Example:
    ```python
    log_element = ui.log()
    callback_handler = NiceGuiLogElementCallbackHandler(log_element)
    app.register_callback_handler(callback_handler)
    ```

    Attributes:
        log (ui.log): The log element to write the messages to.

    Methods:
        on_chain_start(serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
            Called when entering a chain. Prints a message indicating the start of a new chain.

        on_chain_end(outputs: Dict[str, Any], **kwargs: Any) -> None:
            Called when finishing a chain. Prints a message indicating the end of the chain and the outputs.

        on_agent_action(action: AgentAction, **kwargs: Any) -> Any:
            Called on agent action. Writes the action log to the log element.

        on_tool_end(output: str, observation_prefix: Optional[str] = None, llm_prefix: Optional[str] = None, **kwargs: Any) -> None:
            Called when a tool ends. Prints the output and optional observation and LLM prefixes.

        on_text(text: str, **kwargs: Any) -> None:
            Called when agent ends. Writes the text to the log element.

        on_agent_finish(finish: AgentFinish, **kwargs: Any) -> None:
            Called on agent finish. Writes the finish log to the log element.
    """

    def __init__(self, log_element: ui.log) -> None:
        """Initialize callback handler.

        Args:
            log_element (ui.log): The log element to write the messages to.
        """
        self.log = log_element

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we are entering a chain.

        Args:
            serialized (Dict[str, Any]): The serialized chain information.
            inputs (Dict[str, Any]): The inputs to the chain.
            **kwargs (Any): Additional keyword arguments.
        """
        self.log.push(f'\n\n> Entering new {serialized["id"][-1]} chain...')

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain.

        Args:
            outputs (Dict[str, Any]): The outputs of the chain.
            **kwargs (Any): Additional keyword arguments.
        """
        self.log.push('\n> Finished chain.')
        self.log.push(f'\nOutputs: {outputs}')

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action.

        Args:
            action (AgentAction): The agent action.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Any: The result of the agent action.
        """
        self.log.push(action.log)

    def on_tool_end(self,
                    output: str,
                    observation_prefix: Optional[str] = None,
                    llm_prefix: Optional[str] = None,
                    **kwargs: Any,
                    ) -> None:
        """If not the final action, print out observation.

        Args:
            output (str): The output of the tool.
            observation_prefix (Optional[str], optional): The observation prefix. Defaults to None.
            llm_prefix (Optional[str], optional): The LLM prefix. Defaults to None.
            **kwargs (Any): Additional keyword arguments.
        """
        if observation_prefix is not None:
            self.log.push(f'\n{observation_prefix}')
        self.log.push(output)
        if llm_prefix is not None:
            self.log.push(f'\n{llm_prefix}')

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Run when agent ends.

        Args:
            text (str): The agent text.
            **kwargs (Any): Additional keyword arguments.
        """
        self.log.push(text)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end.

        Args:
            finish (AgentFinish): The agent finish.
            **kwargs (Any): Additional keyword arguments.
        """
        self.log.push(finish.log)

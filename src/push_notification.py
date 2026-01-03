from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
import os

from transformers.tools.base import Tool

# Description for the tool
PUSH_NOTIFICATION_DESCRIPTION = (
    "This is a tool that sends a push notification using Expo. It takes two inputs: "
    "`token`, which is the Expo push token of the recipient, and `message`, which is the "
    "message to send. It does not return any output."
)

class PushNotificationTool(Tool):
    description = PUSH_NOTIFICATION_DESCRIPTION
    name = "push_notification"
    inputs = ["text", "text"]
    outputs = []

    def __call__(self, token:str, message:str):
        try:
            # Replace 'your_expo_token' with your actual Expo push notification token
            response = PushClient().publish(
                PushMessage(to=token, body=message)
            )
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            print(f"Error: {exc.errors}")
            raise
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            print("Device not registered.")
            # Add logic to handle inactive push token in your application
        except PushTicketError as exc:
            # Encountered some other per-notification error.
            print(f"Push ticket error: {exc.push_response._asdict()}")
            raise

        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception flows.
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            print("Device not registered.")
            # Add logic to handle inactive push token in your application
        except PushTicketError as exc:
            # Encountered some other per-notification error.
            print(f"Push ticket error: {exc.push_response._asdict()}")
            raise

        return None  # No output is expected

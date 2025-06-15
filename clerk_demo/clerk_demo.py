import reflex_clerk_api as clerk
import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()


class State(rx.State):
    """Basic app state."""

    pass


def index() -> rx.Component:
    return rx.container(
        clerk.clerk_loaded(
            clerk.signed_in(
                rx.vstack(
                    rx.text(
                        "Welcome! You are signed in.", class_name="text-xl font-bold"
                    ),
                    rx.text(
                        f"User: {clerk.ClerkUser.first_name} {clerk.ClerkUser.last_name}"
                    ),
                    rx.text(f"Email: {clerk.ClerkUser.email_address}"),
                    clerk.sign_out_button(
                        rx.button(
                            "Sign out",
                            class_name="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded",
                        )
                    ),
                    spacing="4",
                    align="center",
                ),
            ),
            clerk.signed_out(
                rx.vstack(
                    rx.text(
                        "Please sign in to continue", class_name="text-xl font-bold"
                    ),
                    clerk.sign_in_button(
                        rx.button(
                            "Sign in",
                            class_name="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded",
                        )
                    ),
                    clerk.sign_up_button(
                        rx.button(
                            "Sign up",
                            class_name="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded",
                        )
                    ),
                    spacing="4",
                    align="center",
                ),
            ),
            class_name="flex flex-col items-center justify-center min-h-screen p-8",
        ),
        clerk.clerk_loading(
            rx.vstack(
                rx.text("Loading...", class_name="text-lg"),
                rx.spinner(size="3"),
                align="center",
                class_name="flex flex-col items-center justify-center min-h-screen",
            )
        ),
        class_name="max-w-md mx-auto",
    )


# Create the app
app = rx.App()

# Use clerk.wrap_app instead of clerk.clerk_provider inside the component
clerk.wrap_app(
    app,
    publishable_key=os.environ["CLERK_PUBLISHABLE_KEY"],
    secret_key=os.environ.get("CLERK_SECRET_KEY"),
    register_user_state=True,
)

# Add the page to the app
app.add_page(index, route="/", title="Clerk Demo")

# Add the default sign-in and sign-up pages
clerk.add_sign_in_page(app)
clerk.add_sign_up_page(app)

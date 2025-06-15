import reflex_clerk_api as clerk
import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()


class State(rx.State):
    """Basic app state."""

    debug_info: str = "Debug info will appear here..."
    clerk_state_info: str = "Clerk state info..."

    @rx.event
    async def debug_clerk_state(self):
        """Debug Clerk state information"""
        try:
            clerk_state = await self.get_state(clerk.ClerkState)
            self.clerk_state_info = f"""
ClerkState.auth_checked: {clerk_state.auth_checked}
ClerkState.is_signed_in: {clerk_state.is_signed_in}
ClerkState.user_id: {clerk_state.user_id}
State.is_hydrated: {self.is_hydrated}
            """

            # Also try to get ClerkUser state
            try:
                clerk_user_state = await self.get_state(clerk.ClerkUser)
                user_state_info = f"""
ClerkUser.first_name: "{clerk_user_state.first_name}"
ClerkUser.last_name: "{clerk_user_state.last_name}"
ClerkUser.email_address: "{clerk_user_state.email_address}"
ClerkUser.username: "{clerk_user_state.username}"
ClerkUser.has_image: {clerk_user_state.has_image}
ClerkUser.image_url: "{clerk_user_state.image_url}"
                """
                self.debug_info = f"ClerkUser State:\n{user_state_info}"
            except Exception as user_e:
                self.debug_info = f"Error getting ClerkUser state: {str(user_e)}"

        except Exception as e:
            self.clerk_state_info = f"Error getting ClerkState: {str(e)}"

    @rx.event
    async def check_user_data_availability(self):
        """Check what user data is actually available"""
        try:
            clerk_state = await self.get_state(clerk.ClerkState)
            clerk_user_state = await self.get_state(clerk.ClerkUser)

            self.debug_info = f"""
=== CLERK STATE ===
Is signed in: {clerk_state.is_signed_in}
User ID: {clerk_state.user_id}
Auth checked: {clerk_state.auth_checked}

=== CLERK USER STATE ===
First name: "{clerk_user_state.first_name}" (length: {len(clerk_user_state.first_name or "")})
Last name: "{clerk_user_state.last_name}" (length: {len(clerk_user_state.last_name or "")})
Email: "{clerk_user_state.email_address}" (length: {len(clerk_user_state.email_address or "")})
Username: "{clerk_user_state.username}" (length: {len(clerk_user_state.username or "")})
Has image: {clerk_user_state.has_image}
Image URL: "{clerk_user_state.image_url}"

=== DIRECT ACCESS (should be same as above) ===
Direct first_name: "{clerk.ClerkUser.first_name}"
Direct email: "{clerk.ClerkUser.email_address}"
Direct user_id from ClerkState: "{clerk.ClerkState.user_id}"
            """
        except Exception as e:
            self.debug_info = f"Error in check_user_data_availability: {str(e)}"


def index() -> rx.Component:
    return rx.container(
        clerk.clerk_loaded(
            clerk.signed_in(
                rx.vstack(
                    rx.text(
                        "✅ Welcome! You are signed in.",
                        class_name="text-xl font-bold text-green-600",
                    ),
                    # Debug button
                    rx.button(
                        "Check User Data",
                        on_click=State.check_user_data_availability,
                        class_name="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded",
                    ),
                    # Show comprehensive debug info
                    rx.card(
                        rx.vstack(
                            rx.text(
                                "Complete Debug Info:",
                                class_name="font-semibold text-blue-700",
                            ),
                            rx.text(
                                State.debug_info,
                                class_name="text-xs font-mono whitespace-pre-line bg-gray-100 p-2 rounded",
                            ),
                            spacing="2",
                        ),
                        class_name="bg-blue-50 p-4 rounded-lg border border-blue-200",
                    ),
                    # Show what we can access directly
                    rx.card(
                        rx.vstack(
                            rx.text(
                                "Direct ClerkUser Property Access:",
                                class_name="font-semibold text-green-700",
                            ),
                            rx.hstack(
                                rx.text("First Name:", class_name="font-semibold"),
                                rx.text(
                                    rx.cond(
                                        clerk.ClerkUser.first_name,
                                        clerk.ClerkUser.first_name,
                                        "❌ Empty/None",
                                    ),
                                    class_name="font-mono bg-gray-100 px-2 py-1 rounded",
                                ),
                                spacing="2",
                            ),
                            rx.hstack(
                                rx.text("Last Name:", class_name="font-semibold"),
                                rx.text(
                                    rx.cond(
                                        clerk.ClerkUser.last_name,
                                        clerk.ClerkUser.last_name,
                                        "❌ Empty/None",
                                    ),
                                    class_name="font-mono bg-gray-100 px-2 py-1 rounded",
                                ),
                                spacing="2",
                            ),
                            rx.hstack(
                                rx.text("Email:", class_name="font-semibold"),
                                rx.text(
                                    rx.cond(
                                        clerk.ClerkUser.email_address,
                                        clerk.ClerkUser.email_address,
                                        "❌ Empty/None",
                                    ),
                                    class_name="font-mono bg-gray-100 px-2 py-1 rounded",
                                ),
                                spacing="2",
                            ),
                            rx.hstack(
                                rx.text("Username:", class_name="font-semibold"),
                                rx.text(
                                    rx.cond(
                                        clerk.ClerkUser.username,
                                        clerk.ClerkUser.username,
                                        "❌ Empty/None",
                                    ),
                                    class_name="font-mono bg-gray-100 px-2 py-1 rounded",
                                ),
                                spacing="2",
                            ),
                            rx.hstack(
                                rx.text("Has Image:", class_name="font-semibold"),
                                rx.text(
                                    f"{clerk.ClerkUser.has_image}",
                                    class_name="font-mono bg-gray-100 px-2 py-1 rounded",
                                ),
                                spacing="2",
                            ),
                            spacing="3",
                        ),
                        class_name="bg-green-50 p-4 rounded-lg border border-green-200",
                    ),
                    # Environment check
                    rx.card(
                        rx.vstack(
                            rx.text(
                                "Environment Check:",
                                class_name="font-semibold text-gray-700",
                            ),
                            rx.text(
                                f"✅ Has CLERK_PUBLISHABLE_KEY: {bool(os.environ.get('CLERK_PUBLISHABLE_KEY'))}",
                                class_name="text-sm font-mono",
                            ),
                            rx.text(
                                f"✅ Has CLERK_SECRET_KEY: {bool(os.environ.get('CLERK_SECRET_KEY'))}",
                                class_name="text-sm font-mono",
                            ),
                            spacing="2",
                        ),
                        class_name="bg-gray-50 p-4 rounded-lg border border-gray-200",
                    ),
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
                        "❌ Please sign in to continue",
                        class_name="text-xl font-bold text-gray-700",
                    ),
                    rx.text(
                        "Try using: test+clerk_test@gmail.com with password: test-clerk-password",
                        class_name="text-sm text-gray-500 mb-4",
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
                rx.text("⏳ Loading Clerk...", class_name="text-lg"),
                rx.spinner(size="3"),
                align="center",
                class_name="flex flex-col items-center justify-center min-h-screen",
            )
        ),
        class_name="max-w-4xl mx-auto",
    )


# Create the app
app = rx.App()

# Use clerk.wrap_app instead of clerk.clerk_provider inside the component
clerk.wrap_app(
    app,
    publishable_key=os.environ["CLERK_PUBLISHABLE_KEY"],
    secret_key=os.environ.get("CLERK_SECRET_KEY"),
    register_user_state=True,  # This is crucial for ClerkUser state to work
)

# Add the page to the app
app.add_page(index, route="/", title="Clerk Demo - Debug")

# Add the default sign-in and sign-up pages
clerk.add_sign_in_page(app)
clerk.add_sign_up_page(app)

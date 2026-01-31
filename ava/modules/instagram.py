class InstagramModule:
    def __init__(self):
        self.auto_comment_enabled = True
        self.comment_templates = [
            "Great post! 🔥",
            "Love this! ❤️",
            "Keep it up! 🙌",
            "Amazing work! 👏"
        ]

    def set_auto_comment(self, enabled):
        self.auto_comment_enabled = enabled

    def comment_on_post(self, post_url, comment=None):
        if not comment:
            import random
            comment = random.choice(self.comment_templates)

        if self.auto_comment_enabled:
            return f"Auto-commenting on {post_url}: '{comment}'"
        return f"Auto-comment is disabled for {post_url}."

    def follow_user(self, username):
        return f"Following user {username} on Instagram."

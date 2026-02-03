from ava.modules.instagram import InstagramModule

def test_instagram():
    ig = InstagramModule()

    comment = ig.auto_comment("post123", "scenic_views")
    assert "Amazing post" in comment
    print(f"Comment: {comment}")

    print("Instagram verification successful.")

if __name__ == "__main__":
    test_instagram()

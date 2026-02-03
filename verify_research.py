from ava.modules.research import ResearchModule

def test_research():
    researcher = ResearchModule()

    summary = researcher.research("Python programming")
    assert "Python" in summary
    print(f"Summary: {summary}")

    print("Research verification successful.")

if __name__ == "__main__":
    test_research()

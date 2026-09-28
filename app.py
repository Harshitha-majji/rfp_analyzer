from sample_data import sample_rfp, past_memories
from proposal_generator import generate_proposal
from llm import generate_with_llm


def main():

    print("=" * 70)
    print("PROPOSAL GENERATOR — MEMBER 4")
    print("=" * 70)

    print("\nGenerating proposal using OpenRouter...")
    print("Please wait...\n")

    result = generate_proposal(
        sample_rfp,
        past_memories,
        generate_with_llm
    )

    print("=" * 70)
    print("GENERATED PROPOSAL")
    print("=" * 70)

    print(result["proposal"])

    print("\n" + "=" * 70)
    print(
        f"Historical memories used: "
        f"{result['memory_count']}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()
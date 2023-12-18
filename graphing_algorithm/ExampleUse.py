# Import the tools
import SelectionTools as st

# Create a Value Dictionary instance and load the stored data
vd = st.ValueDictionary(filename="value_dictionary.json")

# Create a Knowledge Base instance and load the stored data
kb = st.KnowledgeBase(filename="knowledge_base.json")

# Create a prompt
prompt = "I want to see GDP from January to March over time."
print("Prompt: " + prompt + "\n")

# Search for all words in the prompt that are also found in the Value Dictionary
# Get a list of all matches returned
matches = vd.search_matches(prompt)
print("Matches: " + str(matches) + "\n")

# Get chosen items from the matches
# For the purposes of this example, it is assumed that the user chooses all the matching words
chosen = matches

# Use the knowledge base to get graph recommendations with the chosen words while using the Value Dictionary
# This will give us back a list of tuples containing recommended graphs
# Each tuple in the list is a matching set of graph recommendation based on different permutations of the input words
# Each item in the tuple is a recommended graph ordered from most recommended to least recommended
recommendations = kb.recommend(vd, chosen)

print("Recommended Graphs: ")
# Looping through list of recommendation sets
for i, tup in enumerate(recommendations):
    print(f"Graph Set {i+1}")
    # Looping through the recommended graphs
    for j, item in enumerate(tup):
        print(f'{j+1}: {item}')
    print()
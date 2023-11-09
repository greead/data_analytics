# Selection Tools
The selection tools module includes several tools for decoding plain-text words and getting recommendations for graphing. Below you will find all of the necessary documentation for using the selection tools.

## Importing the tools
You can import the tools using the following statement as long as the tools are in the same directory:
```
import SelectionTools as st
```

## The Value Dictionary
In order to decode words into parameters that can be used to recommend graphs, you need to use the value dictionary. The value dictionary can primarily be used to search a prompt for matching words in the dictionary. In addition to this, it is necessary to be passed into the knowledge base for decoding purposes.

### Loading the value dictionary
To begin using the value dictionary, you must create a new instance of it and pass in the file name of the saved value dictionary.
```
vd = st.ValueDictionary(filename="value_dictionary.json")
```

### Searching the value dictionary for matching words from a prompt
Given a prompt, we are able to search each word for matches in the value dictionary.
```
matches = vd.search_matches(prompt)
```

## The Knowledge Base
The knowledge base is responsible for recommending graphs to the user. It does this by decoding selected words using a given value dictionary then searching a knowledge base for all graphs that match each combination and permutation of the decoded values.

### Loading the knowledge base
To begin using the knowledge base, you must create a new instance of it and pass in the file name of the saved knowledge base.
```
kb = st.KnowledgeBase(filename="knowledge_base.json")
```

### Recommending graphs
Given a list of selected words and a value dictionary for searching, we are able to receive a list of graph recommendation sets for each available combination and permutation.
```
recommendations = kb.recommend(vd, chosen)
```


"""
Trie (Prefix Tree) Data Structure
Used for efficient prefix matching, vocabulary indexing, and autocomplete.
Time Complexity:
- Insert: O(L) where L is length of word
- Search / StartsWith: O(L)
Space Complexity: O(Total characters in vocabulary)
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

class VocabularyTrie:
    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0

    def insert(self, word: str) -> None:
        """Insert a word into the trie, updating its occurrence frequency."""
        word = word.lower().strip()
        if not word:
            return

        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]

        if not current.is_end_of_word:
            current.is_end_of_word = True
            self.total_words += 1
        current.frequency += 1

    def search(self, word: str) -> bool:
        """Return True if the exact word is present in the vocabulary."""
        word = word.lower().strip()
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word

    def starts_with(self, prefix: str) -> list[str]:
        """Return all words starting with the given prefix."""
        prefix = prefix.lower().strip()
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        results = []
        self._dfs(current, list(prefix), results)
        return results

    def _dfs(self, node: TrieNode, path: list[str], results: list[str]) -> None:
        if node.is_end_of_word:
            results.append("".join(path))

        for char, child_node in sorted(node.children.items()):
            path.append(char)
            self._dfs(child_node, path, results)
            path.pop()

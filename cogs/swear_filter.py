import discord
import codecs
from discord.ext import commands
import datetime
import json
from collections import deque


client = discord.Client(intents=discord.Intents().all())

f = open('censore.txt', 'r', encoding='utf-8')
now = [f.read().strip().split(", ")]
censored_words = now[0]
f.close()

class TrieNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []

def build_trie(keywords):
    root = TrieNode()
        
    for keyword in keywords:
        node = root
        for char in keyword:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.output.append(keyword)
        
    return root

def build_fail_transitions(root):
    queue = deque()
    for node in root.children.values():
        queue.append(node)
        node.fail = root
        
    while queue:
        current_node = queue.popleft()
            
        for key, child in current_node.children.items():
            queue.append(child)
            fail_node = current_node.fail
            while fail_node is not None and key not in fail_node.children:
                fail_node = fail_node.fail
            child.fail = fail_node.children[key] if fail_node else root
            child.output += child.fail.output

def aho_corasick(text, keywords):
    root = build_trie(keywords)
    build_fail_transitions(root)
        
    current_state = root
    results = []
        
    for i, char in enumerate(text):
        while current_state is not None and char not in current_state.children:
            current_state = current_state.fail
        if current_state is None:
            current_state = root
            continue
            
        current_state = current_state.children[char]
            
        for keyword in current_state.output:
            results.append((i - len(keyword) + 1, keyword))
            return results
        
    return results

class SwearDetect(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        
        s = message.content.lower()
        results = aho_corasick(s, censored_words)
        if (len(results) != 0):
            await message.delete()
                
        

async def setup(bot):
    await bot.add_cog(SwearDetect(bot))

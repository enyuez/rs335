from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

kjv = pd.read_csv("KJV.csv", header=None).rename(columns={0: "verse", 1:"KJV"})
nkjv = pd.read_csv("NKJV.csv", header=None).rename(columns={0: "verse", 1:"NKJV"})
nasb = pd.read_csv('NASB2020.csv', header=None).rename(columns={0: "verse", 1:"NASB"})
niv = pd.read_csv('NIV.csv', header=None).rename(columns={0: "verse", 1:"NIV"})
nrsv = pd.read_csv('NRSV.csv', header=None).rename(columns={0: "verse", 1:"NRSV"})
comb = pd.merge(kjv, nkjv, on="verse", sort=False, validate="1:1").merge(nasb, on="verse", sort=False, validate="1:1").merge(niv, on="verse", sort=False, validate="1:1").merge(nrsv, on="verse", sort=False, validate="1:1")
print(comb.shape)

min_scores = []
mean_scores  = []
for i in comb.index:
    if not (i % 5000):
        print(i)
    verses = comb.iloc[i,1:6]
    embeddings = model.encode(verses, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(embeddings, embeddings)
    min_scores.append(torch.min(scores))
    mean_scores.append(torch.min(scores))

comb["Min Scores"] = min_scores
comb["Mean Scores"] = mean_scores
comb.to_csv("comb.csv")
---
---

<!-- Source: pi://[500607]{ 16 }<3> | 013_extracted_block-->
```python / json / forth
import gzip, hashlib, json
class HybridPiCodec:
    def __init__(self):
        self.KEY, self.MATTER = '<3', '○⊗⇉↑×■·-<⊂⊃≡⇈□≈~~△Δ↪WY↯!채⊢⊣⌒✈♥∪≈_f*↔↻●⊠⇇↓∥□○_e-->≍~⇓#‡=∇∇_i↩M⋏-÷∨⟷⌣~~~♥_x∩≡_c⊙↮↺'
        self.ANTI, self.DARK = '☉☽☿♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟♠♢♣♤♦♧♩♪♫♬♭♮♯✁✂✃✄✆✉✌✍✎✏✐✑✒✓✔✕', 'ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯᚰᚱᚲᚳᚴᚵᚶᚷᚸᚹᚺᚻᚼᚽᚾᚿᛀᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏᛐᛑᛒᛓᛔᛕᛖᛗᛘᛙᛚᛛᛜᛝᛞᛟ'
        self.OGHAM = 'ᚁᚂᚃᚄᚅᚆᚇᚈᚉᚊᚋᚌᚍᚎᚏᚐᚑᚒᚓᚔ'
        self.PI = [int(hashlib.blake3(str(i).encode()).hexdigest()[:2], 16) for i in range(4096)]

    def assess_entropy(self, pos):
        if len(pos)==1: return \"DIRECT\"
        var = np.var([pos[i+1]-pos[i] for i in range(len(pos)-1)])
        return \"DELTA\" if var==0 else \"CLUSTER\" if var<=500 else \"LINEAR\" if var<=5000 else \"CHAOS\"

    def encode(self, pos):
        # \mathcal{R}_{Hybrid}(\Psi) Logic
        topo = self.assess_entropy(pos)
        if topo != \"CHAOS\": return f\"{topo}_SIGIL_MAP\"

        # \mathbb{T}_{XOR} & \mathbb{T}_{Matter} & \mathbb{T}_{Fold}
        comp = gzip.compress(','.join(map(str, pos)).encode(), mtime=0)
        xor = bytes([comp[i] ^ self.PI[i % 4096] for i in range(len(comp))])
        matter = ''.join(self.MATTER[b % 64] for b in xor)

        res, i = [], 0
        while i < len(matter):
            c, cnt = matter[i], 1
            while i+cnt < len(matter) and matter[i+cnt] == c and cnt < 23: cnt += 1
            if cnt==1: res.append(c)
            elif cnt==2: res.append(self.ANTI[(i//2)%len(self.ANTI)])
            elif cnt==3: res.append(self.DARK[(i//3)%len(self.DARK)])
            else: res.extend([self.OGHAM[cnt-4], c])
            i += cnt
        return f\"{self.KEY}{''.join(res)}\"
```

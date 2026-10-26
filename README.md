# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** 
searches the listing data using keyword discription by size and price
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
description (str), keywords like "vintage graphic tee"; size (str), like "M" or "W30 L30"; max_price(float), like 30.0
- **Returns:**
list of listing dicts that match all three inputs...each dict has id, title, description, category, style_tags, size, condition, price, colors, brand, and platform.
- **When it has nothing:** Returns an empty list `[]`, not None and not an exception.
- **When it has nothing:**
When there is nothing it will return an empty list, not None, and not an exception

### `suggest_outfit`

- **What it does:**
suggests 1 or 2 outfits based on the thrifted item and user's wardrobe
- **Inputs:**
a list of dict called 'new_item' of what the item the user is considering and a wardrobe dict w/ an 'items' key holding a list
- **Returns:**
returns non empty str w/ outfit suggestions
- **When it has nothing:**
For empty wardrobe returns general styling advice than an empty str

### `create_fit_card`

- **What it does:**
writes a short caption somebody would post about the find
- **Inputs:**
str called 'outfit' for outfit suggestion and a listing dicr for the item 'new_item'
- **Returns:**
str:2-4 sentence caption
- **When it has nothing:**
returns a descriptive msg if 'outfit' is empty or a whitespace than raising

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
**Branch rule:** if search_listings returns an empty list put a message in the session that tells the user what to change (a higher max price, a different size, or fewer keywords) and stop without calling suggest_outfit. Otherwise, take the first result, save it as session["selected_item"], and go to suggest_outfit

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Outfit one leans into classic grunge. Pair the Graphic Tee — 2003 Tour Bootleg Style with the baggy straight-leg jeans, dark wash, and layer the vintage black denim jacket on top. Finish the look with the black combat boots and the black crossbody bag for an effortless, edgy streetwear vibe.

Outfit two plays with proportions. Tuck the Graphic Tee — 2003 Tour Bootleg Style into the wide-leg khaki trousers, cinched with the brown leather belt. Throw the oversized grey crewneck sweatshirt over your shoulders for texture, and complete the outfit with the chunky white sneakers and the black crossbody bag for a casual, effortless everyday look.

  Fit card: Scored this moody 2003 tour bootleg style graphic tee on Depop for just $24, and it has the absolute best faded wash. I'm obsessed with how heavy and worn-in the cotton feels. It's giving total 90s grunge without even trying. #thrifted #grunge #depopfinds

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; r = search_listings('graphic tee', max_price=30); print(len(r)); [print(x['id'], x['title'], x['price'], x['size']) for x in r]"
6
lst_006 Graphic Tee — 2003 Tour Bootleg Style 24.0 L
lst_002 Y2K Baby Tee — Butterfly Print 18.0 S/M
lst_033 Vintage Band Tee — Faded Grey 19.0 L
lst_015 Vintage Graphic Hoodie — Faded Black 26.0 L
lst_017 Mesh Long-Sleeve Top — Black 15.0 S/M
lst_011 Low-Rise Cargo Pants — Khaki 27.0 W29

$ python -c "from tools import search_listings; print(search_listings('ballgown tuxedo', max_price=1))"
[]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
For an effortless everyday streetwear look, pair the Vintage Levi's 501 Jeans — Medium Wash with the white ribbed tank top, layered under the oversized grey crewneck sweatshirt. Add the chunky white sneakers and the black crossbody bag for a casual finish.

For a moodier edge, style the vintage denim with the black cropped zip hoodie and the black combat boots. Cinch the waist with the brown leather belt and throw on the vintage black denim jacket to complete a double-denim fit.
```

```
$ AI201_CACHE=0 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these vintage Levi's 501s on Depop for just $38 and I am never taking them off. They've got that perfect worn-in indigo wash and relaxed streetwear vibe that looks so effortless with just a crisp pair of white sneakers. Truly peak effortless denim energy.

#thrifted #levis501 #depopfinds
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

| Criterion                                              | Target           | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict   |
|---                                                     |---               |---    |---    |---    |---    |---    |---        |
| 1. Matching query completes all three tools            | 4 of 5           | PASS  | PASS  | FAIL  | PASS  | PASS  | MET (4/5) |
| 2. Impossible query stops before suggest_outfit        | 5 of 5           | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 3. Selected item id matches id suggest_outfit received | 5 of 5           | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 4. Fit card mentions the item's price                  | 4 of 5           | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 5. Empty wardrobe still gets outfit advice             | 5 of 5 (revised) | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |

**Real output from one try per criterion** (`agent.py::run_agent`, run by `run_eval.py::main`, full log in `results/run_2026-10-26_0139_before.md`)

**Criterion 1, try 3 (the one FAIL):**
```
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print … +7 more
      →    branch: found results, selected lst_006
[3] model unavailable
      →    stopped, handler set session['error']
```
- stopped early: yes — Couldn't reach the AI model, so no outfit or caption could be written. Check that GEMINI_API_KEY in your .env file is correct, then try again in a minute.

**Criterion 2, try 1:**
```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty, stopping before suggest_outfit
```
- stopped early: yes — Nothing matched 'designer ballgown' in size XXS under $5. Try to raise your max price, or drop the size or try a nearby one, or use fewer or more general keywords (like 'dress' instead of 'ballgown').

**Criterion 3, try 1:**
```
[2] search_listings (via MCP)
      out: 10 items: 90s Leather Bomber — Black, Platform Mary Janes — Black Patent, Oversized Flannel Shirt — Plaid Red/Black … +7 more
      →    branch: found results, selected lst_022
[3] suggest_outfit
      in:  {'new_item': 'lst_022', 'wardrobe_items': 10}
```

**Criterion 4, try 1** (item price is $42.0):
```
Scored this vintage Wrangler denim jacket on Poshmark for just $42 and I am already obsessed with the wash. It's got that perfectly broken-in, effortless streetwear vibe that makes throwing an outfit together way too easy. Can't wait to live in this all season long! #thriftfind #denimstyle #poshmarkfinds
```

**Criterion 5, try 1:**
```
[3] suggest_outfit
      in:  {'new_item': 'lst_007', 'wardrobe_items': 0}
      out: Pair this vintage Wrangler jacket with a black ribbed crop top and high-waisted, wide-leg olive green cargo pa…
```

---


| Criterion                                              | Target           | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict   |
|---                                                     |---               |---    |---    |---    |---    |---    |---        |
| 1. Matching query completes all three tools            | 4 of 5           | PASS  | PASS  | FAIL  | PASS  | PASS  | MET (4/5) |
| 2. Impossible query stops before suggest_outfit        | 5 of 5           | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 3. Selected item id matches id suggest_outfit received | 5 of 5           | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 4. Fit card mentions the item's price                  | 4 of 5           | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 5. Empty wardrobe still gets outfit advice             | 5 of 5 (revised) | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) | - this is what it looks like?






**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (4/5) | Tries 1, 2, 4, 5 returned a fit card. Try 3 stopped at step 3 with the model-unavailable message. |
| 2 | Impossible query stops before suggest_outfit | 5 of 5 | MET (5/5) | All five traces end at step 2 with `[] (empty)` and the branch note, and fit_card stayed None. |
| 3 | Selected item id matches id suggest_outfit received | 5 of 5 | MET (5/5) | Every trace shows `selected lst_022` in step 2 and `'new_item': 'lst_022'` in step 3. |
| 4 | Fit card mentions the item's price | 4 of 5 | MET (5/5) | The item was $42 and all five captions said "$42". |
| 5 | Empty wardrobe still gets outfit advice | 5 of 5 (revised) | MET (5/5) | All five show `'wardrobe_items': 0` and still returned non-empty advice and a fit card, no crash. |

**Diagnoses**

Nothing missed, but criterion 1's one FAIL is worth explaining because it didn't fail the way I expected. My reason for allowing a miss was that keyword search might not match phrasings like "t-shirt" vs "tee." That never happened. Search found the right item all five times. The failure was in the model step: on try 3, `suggest_outfit` couldn't reach the model and my `ModelUnavailable` handler in `agent.py::run_agent` stopped the run with a message. The handler worked, but it threw away the actual error, so the trace can't tell me if it was a rate limit, a timeout, or something else. That's a gap in my error handling, not my search.

**Were my targets too low?** Honestly, yes for criterion 4. Every caption mentioned the price, so 4 of 5 was easy. If I tightened one, it'd be the fit card: most captions across the run open with "Scored this..." or "Found this...", so something like "for 5 different items, no two fit cards share an opening phrase" would actually test variety. Criterion 5 also only passed after I revised it, since the original had no number


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30' --trace
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print … +7 more
      →    branch: found results, selected lst_006
[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe_items
      out: Outfit one leans into classic grunge. Pair the Graphic Tee — 2003 Tour Bootleg Style with the baggy straight-l…
[4] create_fit_card
      in:  dict with keys: new_item, outfit
      out: Scored this moody 2003 tour bootleg style graphic tee on Depop for just $24, and it has the absolute best fade…
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty, stopping before suggest_outfit
```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** In `agent.py::run_agent`, the `ModelUnavailable` handler now captures the actual error (`except ModelUnavailable as exc`) and adds it to the trace note as "Cause: ...". The user still sees the same message. Only the trace gets the detail.

**Which failure it was meant to fix:** Criterion 1, try 3 in the before run. The handler caught a model failure and stopped cleanly, but threw away the real error, so I couldn't tell whether it was a rate limit, a timeout, or something else.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item id matches id suggest_outfit received | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe still gets outfit advice | 5 of 5 (revised) | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** I can't say it helped, because the failure it targets didn't happen this run. Criterion 1 went from 4/5 to 5/5, but that's because the model happened not to drop out, not because of my change. My change only affects what the trace shows when the model fails, and it never failed. The after run did show something useful though: on criterion 3 try 3, the service pushed back and `generate.py` retried ("attempt 1 of 5") and succeeded. My best guess is the before failure was the same thing with the retries running out, and the new Cause line would confirm that next time it happens.

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->
Nothing missed in either run, but a few things aren't right:

- **The improvement is untested.** The model never failed in the after run, so I haven't seen the Cause line work for real. Next I'd force it with a bad key and check the trace shows the actual error.
- **Criterion 4 is too easy.** Every caption mentioned the price. I'd tighten the fit card criterion to something like "no two fit cards for different items share an opening phrase," since most open with "Scored this..." or "Found this...".
- **Empty wardrobe captions can claim things that aren't true.** In the before run, one empty-wardrobe caption said the jacket "works with literally everything in my closet" when the closet is empty. The prompt doesn't tell the model the user owns nothing.
- **Price formatting is inconsistent** ($24 vs $24.00). Small, but it reads like a product listing sometimes.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

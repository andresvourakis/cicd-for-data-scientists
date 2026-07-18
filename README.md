# CI/CD for Data Scientists: Hands-On Exercise

A small, runnable companion to the article. You'll take a FastAPI service that
already has a CI/CD pipeline wired up, watch the pipeline run on GitHub, and
then break it on purpose to see the safety net catch you. Budget about
**10-15 minutes**.

---

## 1. About this repo

This is the same churn service from the FastAPI lesson, with one thing added: a
**CI/CD pipeline** in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
That's the whole idea of this exercise. You already built the engineering habits
(a service, tests, a reproducible environment). CI/CD is the layer that runs them
for you, automatically, every time you push, instead of you remembering to.

You don't need to write any YAML. You fork the repo, turn Actions on, push a
commit, and watch the pipeline run. The model ships **pre-trained** so everything
runs with no setup.

## 2. Watch the pipeline run (the main event)

This part happens on GitHub, not your laptop.

1. **Fork this repo** to your own GitHub account (top-right **Fork** button).
2. On your fork, open the **Actions** tab and click the button to enable
   workflows (GitHub turns them off on forks until you say so).
3. Make any small change (edit this README) and **commit it to `main`** from the
   GitHub web editor.
4. Back in the **Actions** tab, watch the **CI** run. You'll see two jobs go
   green in order: **test**, then **deploy**.

*You should see:* a yellow dot turn into a green checkmark next to your commit.
Click into the run to watch each step execute: installing the environment,
running the tests, running the linter. That green check is the pipeline telling
you the change is safe.

## 3. Break it on purpose

This is the part that makes it click.

1. Open `tests/test_api.py` on your fork and change one assertion so it's wrong,
   for example change `{"status": "ok"}` to `{"status": "nope"}`.
2. Commit it to `main`.
3. Watch the **Actions** tab again.

*You should see:* the **test** job go **red**, and the **deploy** job never run
(it only runs if the tests pass). Click into the failed run and GitHub points you
at the exact line that broke. Fix the assertion back, push again, and watch it
go green.

That's the loop: the system catches the problem before it ships, so "did I run
the tests?" stops being a question you have to remember to ask.

## 4. Run it locally (optional)

Want to run the service on your own machine too? This project uses
[uv](https://docs.astral.sh/uv/), the same tool as the earlier lessons.

```bash
uv run uvicorn app.main:app --reload   # start the service (Ctrl+C to stop)
uv run pytest                          # run the same tests CI runs
uv run ruff check .                    # run the same linter CI runs
```

Once the server is running, open
[http://localhost:8000/docs](http://localhost:8000/docs) to try the `/predict`
endpoint from your browser.

> **Don't have uv?** Install it in one line:
> `curl -LsSf https://astral.sh/uv/install.sh | sh` (see
> [the docs](https://docs.astral.sh/uv/getting-started/installation/) for other
> platforms). Prefer plain pip? The repo ships a `requirements.txt`:
> `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`,
> then drop the `uv run` prefix from the commands above.

## 5. Going further (optional)

Want to push a little past the article? Try these:

- **Wire up a real deploy.** Right now the `deploy` job is a placeholder. Deploy
  the service to a free host like [Render](https://render.com), grab its deploy
  hook URL, add it as a repository secret named `RENDER_DEPLOY_HOOK`
  (**Settings -> Secrets and variables -> Actions**), and replace the placeholder
  step with:

  ```yaml
  - name: Deploy to Render
    run: curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
  ```

- **Add another check.** Add a test for a new case (say, a very high income) and
  watch CI start enforcing it too.

- **Add CI to your own project.** The real payoff: take a project you already
  have, copy `.github/workflows/ci.yml` into it, and adjust the steps. Even just
  the test step is enough to start.

---

That's it. You've watched a pipeline test your code automatically, seen it block
a broken change, and learned where to add a real deploy. That's CI/CD: the
automation layer that runs your engineering habits for you, every single push.

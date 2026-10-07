# Publishing ysenseai.org on Cloudflare (Workers static assets)

This folder is the source of **https://ysenseai.org**. It is a plain static
site: `public/index.html`, `public/styles.css`, and a few crawler files. No
build step, no server, no database. Cloudflare serves `public/` as a Worker
with static assets, exactly the way `verifimind-peas-landing` serves
verifimind.io (that repo's `DEPLOY.md` is the template for this guide).

**Why now:** the Manus subscription that hosts the current ysenseai.org is
ending. After the steps below, every merge to `main` publishes this folder and
no third-party subscription is involved.

**Important difference from verifimind.io:** the `ysenseai.org` zone also
carries **`verifimind.ysenseai.org`**, the VerifiMind PEAS MCP server on
Google Cloud Run (it is a CNAME to `ghs.googlehosted.com`). That record must
survive the move untouched, or the MCP server goes dark. It is called out at
every step where it matters.

Cloudflare renames menus from time to time. If a label below does not match
exactly, look for the closest equivalent.

---

## Part 0: Find out where the domain lives (10 min, do this first)

1. Find the **registrar** of `ysenseai.org` (where it is renewed). Log in and
   note the **current nameservers**. If they are already
   `*.ns.cloudflare.com`, skip to Part D2 step 2: the zone is on Cloudflare
   and only the records change.
2. Note what currently answers. On 7 Oct 2026 the records were:

   | Name | Type | Value | What it is |
   |---|---|---|---|
   | `ysenseai.org` | A | `216.239.32.21`, `216.239.34.21`, `216.239.36.21`, `216.239.38.21` | Google-hosted web (the Manus-era site) |
   | `www.ysenseai.org` | CNAME | `ghs.googlehosted.com` | Google-hosted web (same site) |
   | `verifimind.ysenseai.org` | CNAME | `ghs.googlehosted.com` | **VerifiMind PEAS MCP server (Cloud Run). Keep.** |

3. Export or screenshot **every** record at the current DNS host, especially
   MX and TXT (email, SPF, DKIM, site verification). Losing these breaks
   email to `@ysenseai.org`.
4. If DNSSEC is on at the registrar, turn it off and wait an hour before
   changing nameservers.

## Part A: Merge, then create the Cloudflare app (about 15 min)

1. **Merge the pull request** that adds this folder to `main`. Nothing public
   changes yet: ysenseai.org keeps pointing at the old host until Part E.
2. Log in at https://dash.cloudflare.com (the same account that runs
   verifimind.io).
3. **Workers & Pages** → **Create** → **Import a repository** → GitHub →
   select `YSense-AI-Attribution-Infrastructure` → **Next**.
4. Fill in **Set up your application**:

   | Field | Value |
   |---|---|
   | Project name | `ysenseai-landing` (must match `name` in `wrangler.jsonc`) |
   | Production branch | `main` |
   | Build command | leave **empty** (there is nothing to build) |
   | Deploy command | `npx wrangler deploy` |
   | Preview command | `npx wrangler preview` |
   | Enable Preview builds | On |
   | Protect with Cloudflare Access | **Off** |
   | Advanced settings → **Root directory / Path** | `website` |
   | Advanced settings → Build watch paths (if offered) | `website/**` so code-only pushes do not redeploy the site |

5. **Deploy.** The log should show wrangler uploading a handful of assets and
   finish with a `https://ysenseai-landing.<your-subdomain>.workers.dev` URL.

## Part B: Check the new site (10 min)

Open the `*.workers.dev` URL on desktop **and** phone, and check:

- [ ] The page loads with its fonts and gradient hero; no white unstyled page
      (that would mean `styles.css` did not upload).
- [ ] The nav toggle works on the phone and the page does not scroll sideways.
- [ ] `/llms.txt`, `/robots.txt` and `/sitemap.xml` open as plain text/XML.
- [ ] `/anything-else` shows the styled "Page not found" page.
- [ ] The "Try the UX Demo", "View on GitHub" and "Read White Paper" buttons
      go where they say.

## Part C: How publishing works from now on

Every push to `main` that touches `website/` rebuilds and publishes the site.
Pushes to other branches create preview versions with their own URLs. Edit
`public/index.html` for copy changes; keep `public/llms.txt` and
`public/sitemap.xml` (`lastmod`) in step when you change the page.

## Part D: Bring ysenseai.org DNS to Cloudflare

Skip D1 to D3 if Part 0 showed the nameservers are already Cloudflare's.

### D1. Add the domain to Cloudflare
1. Cloudflare dashboard home → **Add a domain** → `ysenseai.org` → keep
   **Quick scan for DNS records** → Continue → **Free** plan.
2. Review the imported records against your Part 0 export. Add anything
   missing. **Confirm `verifimind` CNAME `ghs.googlehosted.com` is present**,
   set to **DNS only** (grey cloud); Cloud Run manages its own certificate
   and does not want Cloudflare proxying it.
3. Leave the existing apex `A` records and `www` CNAME in place, **DNS only**
   (grey cloud), so the old site keeps working while nameservers switch.
4. **Continue** → Cloudflare shows two nameservers. Copy them.

### D2. Change nameservers at the registrar
1. At the registrar, replace the current nameservers with the two Cloudflare
   nameservers. Confirm (SMS or email verification may be required).
2. Back in Cloudflare → **Check nameservers now**. Cloudflare emails you when
   the zone is **Active**, usually within 1 to 24 hours.
3. While waiting, open https://verifimind.ysenseai.org/health . It must keep
   answering throughout; if it stops, the `verifimind` CNAME was lost: re-add
   it exactly as in Part 0.

## Part E: Connect the domain to the Worker (once the zone is Active)

1. Cloudflare → `ysenseai.org` → **DNS → Records**: **delete only** the apex
   `A` records (`216.239.x.21`) and the `www` CNAME to `ghs.googlehosted.com`.
   **Do not touch `verifimind`, MX or TXT.**
2. **Workers & Pages** → `ysenseai-landing` → **Settings** → **Domains &
   Routes** → **Add** → **Custom domain** → `ysenseai.org` → Add. Repeat for
   `www.ysenseai.org`. Cloudflare creates the records and the certificate,
   usually within minutes.
3. `ysenseai.org` → **Rules → Redirect Rules** → **Create rule** → template
   **Redirect from WWW to root** → Deploy.
4. `ysenseai.org` → **SSL/TLS → Edge Certificates** → turn on **Always Use
   HTTPS**. Keep the SSL mode at **Full** or **Full (strict)**; do not pick
   Flexible, it breaks the Cloud Run subdomain.

## Part F: Keep AI crawlers allowed

New Cloudflare zones may block AI crawlers by default, which would hide the
site from AI search. On the `ysenseai.org` zone:

1. **AI Crawl Control** (or **Security → Bots**): **Block AI bots** off.
2. **Managed robots.txt** off, so our own `robots.txt` is served unchanged.
3. **Bot Fight Mode** off.

## Part G: Measurement (10 min)

1. **Analytics & Logs → Web Analytics → Add a site** → `ysenseai.org` →
   automatic setup (cookie-free, no code change).
2. **Google Search Console** → Add property → Domain → `ysenseai.org` →
   verify with the DNS TXT record (Cloudflare can add it) → Sitemaps → submit
   `https://ysenseai.org/sitemap.xml`.
3. **Bing Webmaster Tools** → Import from Google Search Console.

## Part H: Final checks, then let Manus go

- [ ] `https://ysenseai.org` and `https://www.ysenseai.org` load the new site
      over HTTPS (www redirects to the root).
- [ ] `https://verifimind.ysenseai.org/health` still answers.
- [ ] `https://ysenseai.org/llms.txt` and `/robots.txt` are served unchanged.
- [ ] Email to `alton@ysenseai.org` still arrives (send yourself one).
- [ ] The Hugging Face Space and the VerifiMind landing page links back to
      ysenseai.org land on the new site.

Then let the Manus subscription lapse. Before it does, download anything on
the old site that is not in this repository (images, copy you want to keep).

## Rollback

- **Bad deploy:** Workers & Pages → `ysenseai-landing` → **Deployments** →
  pick the last good version → **Rollback**.
- **DNS problem:** fix the records in Cloudflare (DNS → Records, and the
  Worker's Domains & Routes). Once Manus has lapsed, pointing the nameservers
  back does not restore the old site.

---

## Reference

### Local check (any machine with Node 22)

```bash
cd website
npx wrangler@4 deploy --dry-run      # validates wrangler.jsonc and lists the assets
python3 -m http.server 8080 -d public  # then open http://localhost:8080
```

### Files

| File | Used for |
|---|---|
| `wrangler.jsonc` | Cloudflare Worker name and the `public/` assets directory |
| `public/index.html`, `public/styles.css` | The page |
| `public/404.html` | Served with status 404 for unknown paths |
| `public/_headers` | Security and caching headers (Cloudflare reads this file) |
| `public/robots.txt`, `public/sitemap.xml`, `public/llms.txt` | Crawler and AI-agent files |

### Rules for changes

- Stay static: no forms posting to a server, no login, no database.
- Keep claims in step with the README's "Known Limitations" section. The
  page says plainly what is built and what is not; keep it that way.
- Never link media on Manus or other temporary hosts. Put images in
  `public/assets/` (WebP or optimised PNG at display size).
- Check 390 px (phone), 1280 px and 1920 px widths. No horizontal scroll.

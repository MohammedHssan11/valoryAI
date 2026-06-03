# pf_scraper/cli.py
import argparse
import os
import json

from .config import ScraperConfig
from .runner import fetch_one_page
from .paginator import paginate_category
from .writer import write_jsonl
from .multi_runner import scrape_all_categories
from .merge import merge_jsonl_files
from .details_fetcher import fetch_listing_next_data
from .details_parser import find_listing_payload, extract_details


def _parse_params(pairs):
    out = {}
    if not pairs:
        return out
    for x in pairs:
        if "=" not in x:
            raise ValueError(f"Bad --param '{x}'. Must be key=value")
        k, v = x.split("=", 1)
        k = k.strip()
        v = v.strip()
        # allow repeated params: bdr[]=3 bdr[]=4
        if k in out:
            if isinstance(out[k], list):
                out[k].append(v)
            else:
                out[k] = [out[k], v]
        else:
            out[k] = v
    return out


def main():
    parser = argparse.ArgumentParser(
        description="PropertyFinder SSR scraper (UAE/EG) - extracts JSON from __NEXT_DATA__"
    )
    parser.add_argument("--country", default="EG", help="EG|UAE (default: EG)")

    sub = parser.add_subparsers(dest="cmd")

    p_one = sub.add_parser("one", help="Fetch one page (debug)")
    p_one.add_argument("--category", default="buy", help="rent|buy|commercial_rent|commercial_buy|new_projects")
    p_one.add_argument("--page", type=int, default=1, help="1-based page number")
    p_one.add_argument("--param", action="append", default=[], help="Extra query params as key=value (repeatable)")

    p_scrape = sub.add_parser("scrape", help="Scrape a category and write JSONL")
    p_scrape.add_argument("--category", default="buy", help="rent|buy|commercial_rent|commercial_buy|new_projects")
    p_scrape.add_argument("--out", default="out.jsonl", help="Output JSONL file path")
    p_scrape.add_argument("--start-page", type=int, default=1)
    p_scrape.add_argument("--max-pages", type=int, default=None)
    p_scrape.add_argument("--sleep-min", type=float, default=0.8)
    p_scrape.add_argument("--sleep-max", type=float, default=1.8)
    p_scrape.add_argument("--checkpoint", default=None)
    p_scrape.add_argument("--param", action="append", default=[], help="Extra query params as key=value (repeatable)")

    p_all = sub.add_parser("scrape-all", help="Scrape ALL categories with resume")
    p_all.add_argument("--out-dir", default="data_eg", help="Output directory")
    p_all.add_argument("--max-pages", type=int, default=None, help="Max pages per category")
    p_all.add_argument("--sleep-min", type=float, default=0.8)
    p_all.add_argument("--sleep-max", type=float, default=1.8)
    p_all.add_argument("--no-resume", action="store_true")

    p_merge = sub.add_parser("merge", help="Merge category JSONL files into one all.jsonl (dedupe)")
    p_merge.add_argument("--in-dir", default="data_eg")
    p_merge.add_argument("--out", default="data_eg/all.jsonl")

    p_details = sub.add_parser("details", help="Fetch listing detail page and extract __NEXT_DATA__ details")
    p_details.add_argument("--url", required=True)

    args = parser.parse_args()
    if args.cmd is None:
        parser.print_help()
        return

    cfg = ScraperConfig(country=args.country)

    if args.cmd == "one":
        extra = _parse_params(args.param)
        fetch_one_page(cfg=cfg, category_name=args.category, page=args.page, extra_filters=extra)
        return

    if args.cmd == "scrape":
        extra = _parse_params(args.param)
        rows = paginate_category(
            cfg=cfg,
            category_name=args.category,
            start_page=args.start_page,
            max_pages=args.max_pages,
            sleep_min=args.sleep_min,
            sleep_max=args.sleep_max,
            checkpoint_path=args.checkpoint,
            extra_filters=extra,
        )
        n = write_jsonl(args.out, rows)
        print(f"Done ✅ Wrote {n} rows to: {args.out}")
        return

    if args.cmd == "scrape-all":
        scrape_all_categories(
            cfg=cfg,
            out_dir=args.out_dir,
            max_pages=args.max_pages,
            sleep_min=args.sleep_min,
            sleep_max=args.sleep_max,
            resume=(not args.no_resume),
        )
        return

    if args.cmd == "merge":
        in_dir = args.in_dir
        cats = ["rent", "buy", "commercial_rent", "commercial_buy", "new_projects"]
        files = [os.path.join(in_dir, f"{c}.jsonl") for c in cats]
        existing_files = [f for f in files if os.path.exists(f)]
        if not existing_files:
            print(f"❌ No files found in {in_dir} to merge.")
            return
        n = merge_jsonl_files(existing_files, args.out)
        print(f"Done ✅ merged {n} rows -> {args.out}")
        return

    if args.cmd == "details":
        res = fetch_listing_next_data(args.url)
        payload, path = find_listing_payload(res.next_data)
        if not payload:
            print("❌ Could not locate listing payload in __NEXT_DATA__.")
            print(f"Found path: {path}")
            return
        details = extract_details(payload)
        details["_debug_found_path"] = path
        details["_source_url"] = args.url
        print(json.dumps(details, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()

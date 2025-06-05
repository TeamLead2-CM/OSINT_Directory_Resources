# OSINT_Directory_Resources

#### Setup and Usage

1. `pip install Willow[Pillow,heif] pandas tqdm cairosvg`

2. start (configure folders etc in code):
`python image_downloader.py --file <input filename>`

3. logs saved in logs.txt. failed entries, etc. retry using the following command:
`python image_downloader.py --file <input filename> --retry`

4. verify and check for missing entries using:
`python verify.py` (change base dir accordingly)
missing entries saved in `missing.txt`

5. generate github links and save in sheet using:
`python github_link_generator.py -i <input filename> -o <output filename>`
output file will be generated: `<inputfilename>_github_links.xlsx`





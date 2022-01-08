# data paths
PATH_REVIEW_NTXT = './data/raw/reviews/no_text/review_page%d.jl'
PATH_REVIEW_TXT = './data/raw/reviews/text/reviewtext_page%d.jl'
PATH_REVIEW_COMB = './data/raw/reviews/combined/page_%d.csv'
PATH_REVIEW_SENTS = './data/prepared/review_sentiments/%s.csv'

# pages
NUM_REVIEW_PAGES = 524

# review text
REVIEW_HIDDEN = '(Review text hidden)'


# review column indices
class ReviewCols:
    UID=0
    GID=1
    POLARITY=2
    TIMESTAMP=3
    PLAYTIME=4
    VOTES_UP=5
    VOTES_FUNNY=6
    TEXT=7

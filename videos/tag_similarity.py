from videos.transcript_score import clean_user_tag_and_split
from scipy import spatial
import tensorflow_hub as hub

embedding = hub.load('universal-sentence-encoder_4')

SIMILARITY_THRESHOLD = 0.8


def is_similar(tag1, tag2):
    tag1_cleaned = ' '.join(clean_user_tag_and_split(tag1))
    tag2_cleaned = ' '.join(clean_user_tag_and_split(tag2))
    embeddings = embedding([tag1_cleaned, tag2_cleaned])
    similarity_grade = 1 - spatial.distance.cosine(embeddings[0], embeddings[1])
    print(similarity_grade)
    return similarity_grade > SIMILARITY_THRESHOLD


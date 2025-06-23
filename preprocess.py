import pandas as pd

def preprocess_articles(input_path='all_articles_scraped.csv', output_path='cleaned_articles.csv'):
    # Load the CSV and skip malformed lines
    df = pd.read_csv(input_path, engine='python', on_bad_lines='skip')

    # Drop rows with missing essential fields
    clean_df = df.dropna(subset=['headline', 'genre', 'article'])

    # Safely create the combined text column
    clean_df.loc[:, 'text'] = clean_df['headline'] + " " + clean_df['article']

    # Select and reorder necessary columns
    final_df = clean_df[['url', 'headline', 'publish_date', 'genre', 'article', 'text']]

    # Save to new CSV with UTF-8-BOM encoding for better compatibility
    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[✅] Cleaned CSV saved as: {output_path} (UTF-8 with BOM for Excel)")

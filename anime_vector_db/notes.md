Properties I want to save:

type Item = {
    mal_id: number;
    type: string;
    name: string;
    url: string;
}
- genres
    shape: Item[]
- themes
    shape: Item[]
- demographics
    shape: Item[]

- synopsis:
    shape?: string
- background:
    shape?: string;
- authors

METADATA:
    - title:
        shape?: string;
    - type:
        shape: string;
    - subtype:
        shape?: string;
    - status:
        shape?: string;
    - score:
        shape?: number;
DOCUMENT:
    shape: `
    synopsis: ${synopsis};\n
    background: ${background};\n
    authors: ${authors};\n
    genres: ${genres};\n
    themes: ${themes};\n
    demographics: ${demographics}`



Available filters:
- type (Anime, Manga, Character)
    List of options
    Multiselect available
    "type": { "$in": ["value1", "value2"] }
- Subtype (TV, ONA, Manhwa, etc)
    List of options
    Multiselect available
    "subtype": { "$in": ["value1", "value2"] }
- Status (Airing, Finished, etc)
    List of options
    Multiselect available
    "status": { "$in": ["value1", "value2"] }
- Authors (Author Name)
    Input field
    Multiselect available
    (filters: string[]) => {
        strubstring = get substring ";authors: '*';"
        authors = split '*' by commas, each is a value
        get all documents where authors include any of the filter elements
    }
- Genres
    List of options/Input field
    Multiselect available
    (filters: string[]) => {
        strubstring = get substring ";genres: '*';"
        genres = split '*' by commas, each is a value
        get all documents where genres include any of the filter elements
    }
- Themes
    List of options/Input field
    Multiselect available
    (filters: string[]) => {
        strubstring = get substring ";themes: '*';"
        themes = split '*' by commas, each is a value
        get all documents where themes include any of the filter elements
    }
- Demographics
    List of options/Input field
    Multiselect available
    (filters: string[]) => {
        strubstring = get substring ";demographics: '*';"
        demographics = split '*' by commas, each is a value
        get all documents where demographics include any of the filter elements
    }

type, subtype and status are included in the chromadb query, the rest of filters are done manually in python

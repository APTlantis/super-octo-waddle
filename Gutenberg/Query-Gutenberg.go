package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

type Book struct {
	ID      int               `json:"id"`
	Title   string            `json:"title"`
	Authors []Person          `json:"authors"`
	Formats map[string]string `json:"formats"`
}

type Person struct {
	Name string `json:"name"`
}

type APIResponse struct {
	Results []Book `json:"results"`
}

func fetchBooks(query string) ([]Book, error) {
	url := "https://gutendex.com/books?" + query
	resp, err := http.Get(url)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch API: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %v", err)
	}

	var apiResponse APIResponse
	err = json.Unmarshal(body, &apiResponse)
	if err != nil {
		return nil, fmt.Errorf("failed to parse JSON: %v", err)
	}

	return apiResponse.Results, nil
}

func main() {
	fmt.Println("📚 Fetching books from Gutendex API...")
	query := "languages=en&author_year_start=1900&copyright=false"
	books, err := fetchBooks(query)
	if err != nil {
		log.Fatal("❌ Error:", err)
	}

	file, _ := json.MarshalIndent(books, "", " ")
	_ = os.WriteFile("gutendex_books.json", file, 0644)

	fmt.Println("✅ Books saved to gutendex_books.json")
}

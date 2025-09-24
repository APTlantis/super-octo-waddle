package main

import (
	"bufio"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"sync"
	"time"
)

// Configuration
const (
	baseURL         = "https://data.commoncrawl.org/" // Base URL for downloading
	outputDir       = "Wet-Files"                     // Directory where downloads will be saved
	pathsFile       = "wet.paths"                     // File containing list of WET files
	maxDownloadSize = 750 * 1024 * 1024 * 1024        // 750GB limit in bytes
)

var totalDownloaded int64 = 0
var mu sync.Mutex // Mutex for safe concurrent updates

// Check if file exists
func fileExists(path string) bool {
	_, err := os.Stat(path)
	return err == nil
}

// Download a single file
func downloadFile(url, destPath string, wg *sync.WaitGroup) {
	defer wg.Done()

	// Skip if file already exists
	if fileExists(destPath) {
		fmt.Println("Skipping (exists):", destPath)
		return
	}

	// Create HTTP request
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Download error:", err)
		return
	}
	defer resp.Body.Close()

	// Check if request was successful
	if resp.StatusCode != http.StatusOK {
		fmt.Println("Failed to download:", url, "Status:", resp.StatusCode)
		return
	}

	// Get file size
	contentLength := resp.ContentLength
	if contentLength <= 0 {
		fmt.Println("Skipping (empty file):", url)
		return
	}

	// Check download limit
	mu.Lock()
	if totalDownloaded+contentLength > maxDownloadSize {
		fmt.Println("Reached 750GB limit. Stopping further downloads.")
		mu.Unlock()
		return
	}
	totalDownloaded += contentLength
	mu.Unlock()

	// Create output directory if missing
	os.MkdirAll(filepath.Dir(destPath), os.ModePerm)

	// Save file
	outFile, err := os.Create(destPath)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer outFile.Close()

	_, err = io.Copy(outFile, resp.Body)
	if err != nil {
		fmt.Println("Error saving file:", err)
		return
	}

	fmt.Println("Downloaded:", destPath, "Size:", strconv.FormatInt(contentLength, 10), "bytes")
}

// Monitor and display total download size
func monitorProgress() {
	for {
		mu.Lock()
		fmt.Printf("Total Downloaded: %.2f GB\n", float64(totalDownloaded)/(1024*1024*1024))
		mu.Unlock()
		time.Sleep(10 * time.Second) // Update every 10 seconds
	}
}

func main() {
	// Open paths file
	file, err := os.Open(pathsFile)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var wg sync.WaitGroup

	// Start progress monitor
	go monitorProgress()

	// Process each file path
	for scanner.Scan() {
		filePath := scanner.Text()
		if filePath == "" {
			continue
		}

		url := baseURL + filePath
		destPath := filepath.Join(outputDir, filepath.Base(filePath))

		wg.Add(1)
		go downloadFile(url, destPath, &wg)

		// Sleep a bit to avoid hammering servers
		time.Sleep(200 * time.Millisecond)
	}

	wg.Wait()
	fmt.Println("All downloads complete or stopped at limit.")
}

package main

import (
	"compress/gzip"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"sync"
)

// Configuration
const (
	inputDir  = "wet_files"    // Folder where .gz files are located
	outputDir = "unzipped_wet" // Destination for extracted files
)

func main() {
	// Ensure output directory exists
	os.MkdirAll(outputDir, os.ModePerm)

	// Find all .gz files, including in subdirectories
	var files []string
	err := filepath.Walk(inputDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			fmt.Println("Error accessing file:", path, err)
			return nil
		}
		if !info.IsDir() && strings.HasSuffix(info.Name(), ".gz") {
			files = append(files, path)
		}
		return nil
	})
	if err != nil {
		fmt.Println("Error scanning for .gz files:", err)
		return
	}

	// If no files found, print error and exit
	if len(files) == 0 {
		fmt.Println("❌ No .gz files found in", inputDir)
		return
	}

	fmt.Println("✅ Found", len(files), ".gz files. Starting extraction...")

	var wg sync.WaitGroup

	// Extract each file concurrently
	for _, gzPath := range files {
		wg.Add(1)
		go unzipFile(gzPath, &wg)
	}

	wg.Wait()
	fmt.Println("✅ All files extracted!")
}

// Unzips a single .gz file
func unzipFile(gzPath string, wg *sync.WaitGroup) {
	defer wg.Done()

	// Determine output file path (remove .gz extension)
	outputPath := filepath.Join(outputDir, strings.TrimSuffix(filepath.Base(gzPath), ".gz"))

	// Skip if already extracted
	if _, err := os.Stat(outputPath); err == nil {
		fmt.Println("Skipping (already extracted):", outputPath)
		return
	}

	// Open .gz file
	gzFile, err := os.Open(gzPath)
	if err != nil {
		fmt.Println("Error opening:", gzPath, err)
		return
	}
	defer gzFile.Close()

	// Create gzip reader
	reader, err := gzip.NewReader(gzFile)
	if err != nil {
		fmt.Println("Error creating gzip reader:", gzPath, err)
		return
	}
	defer reader.Close()

	// Create output file
	outFile, err := os.Create(outputPath)
	if err != nil {
		fmt.Println("Error creating output file:", outputPath, err)
		return
	}
	defer outFile.Close()

	// Copy contents
	_, err = io.Copy(outFile, reader)
	if err != nil {
		fmt.Println("Error extracting:", gzPath, err)
		return
	}

	fmt.Println("Extracted:", outputPath)
}

package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/DevMentalBrain/API-reGECS/api"
)

func main() {
	http.HandleFunc("/health", api.HealthHandler)
	http.HandleFunc("/move", api.MoveHandler)

	port := ":8080"
	fmt.Printf("Server running on port %s\n", port)
	if err := http.ListenAndServe(port, nil); err != nil {
		log.Fatalf("[FATAL]: Failed to start server: %s", err)
	}
}

package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"
)

type response struct {
	VisitorCount []visitorCount
}

type visitorCount struct {
	CountVisitors   int `json:"personCount"`
	MaximumVisitors int `json:"maxPersonCount"`
}

func main() {

	url := "https://api.ticos-systems.cloud/api/gates/counter?organizationUnitIds=30244"

	spaceClient := http.Client{
		Timeout: time.Second * 2, // Timeout after 2 seconds
	}

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		log.Fatal(err)
	}

	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("Accept", "application/json, text/plain, */*")
	req.Header.Set("Abp-TenantId", "2115")
	req.Header.Set("Abp.TenantId", "2115")
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
	req.Header.Set("DNT", "1")
	req.Header.Set("Origin", "https://www.stadtwerke-bamberg.de")
	req.Header.Set("Sec-Fetch-Site", "cross-site")
	req.Header.Set("Sec-Fetch-Mode", "cors")
	req.Header.Set("Sec-Fetch-Dest", "empty")
	req.Header.Set("Referer", "https://www.stadtwerke-bamberg.de/baeder/bambados")
	req.Header.Set("Accept-Language", "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7")

	res, getErr := spaceClient.Do(req)
	if getErr != nil {
		log.Fatal(getErr)
	}

	if res.Body != nil {
		defer res.Body.Close()
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		log.Fatal(readErr)
	}

	body2 := strings.Replace(string(body), "[", "", -1)
	body3 := strings.Replace(body2, "]", "", -1)

	//fmt.Println(body)
	//fmt.Println(body2)
	//fmt.Println(body3)
	textBytes := []byte(body3)
	//fmt.Println(textBytes)

	visitorCount1 := visitorCount{}
	jsonErr := json.Unmarshal(textBytes, &visitorCount1)
	if jsonErr != nil {
		log.Fatal(jsonErr)
	}

	iso8601 := time.Now().Format(time.RFC3339)

	fmt.Println(iso8601 + ";" + strconv.Itoa(visitorCount1.CountVisitors) + ";" + strconv.Itoa(visitorCount1.MaximumVisitors-visitorCount1.CountVisitors) + ";" + strconv.Itoa(visitorCount1.MaximumVisitors))
}

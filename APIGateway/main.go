package main

import (
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
)

// 🚗 차량 인식 서비스의 기본 URL
const licenseServiceURL = "http://license-recognition-service:8001"

// 🧑‍🏭 인원 인식 서비스의 기본 URL
const personServiceURL = "http://person-recognition-service:8002"

// NewReverseProxy는 주어진 대상 URL로 요청을 포워딩하는 ReverseProxy 핸들러를 생성합니다.
func NewReverseProxy(targetURL string) *httputil.ReverseProxy {
	// 대상 URL 파싱
	target, err := url.Parse(targetURL)
	if err != nil {
		log.Fatalf("Failed to parse target URL %s: %v", targetURL, err)
	}

	// ReverseProxy 생성
	proxy := httputil.NewSingleHostReverseProxy(target)

	// 요청을 전달하기 전/후에 추가적인 로직을 삽입할 수 있습니다.
	proxy.Director = func(req *http.Request) {
		req.URL.Scheme = target.Scheme
		req.URL.Host = target.Host
		// Gateway에서 인증/로그 헤더 등을 추가할 수 있습니다.
		// req.Header.Add("X-Gateway-Auth", "validated-token")
	}

	// 에러 핸들링 로직 추가 (선택 사항)
	proxy.ErrorHandler = func(rw http.ResponseWriter, req *http.Request, err error) {
		log.Printf("Proxy error: %v", err)
		http.Error(rw, "Service temporarily unavailable", http.StatusBadGateway)
	}

	return proxy
}

func main() {
	// 1. 차량 인식 서비스용 프록시 설정
	licenseProxy := NewReverseProxy(licenseServiceURL)
	// /v1/license 경로로 들어오는 모든 요청을 licenseProxy가 처리하도록 설정
	http.Handle("/v1/license/", licenseProxy)

	// 2. 인원 인식 서비스용 프록시 설정
	personProxy := NewReverseProxy(personServiceURL)
	// /v1/person 경로로 들어오는 모든 요청을 personProxy가 처리하도록 설정
	http.Handle("/v1/person/", personProxy)

	// 3. (선택 사항) 루트 경로에 Gateway 상태 표시
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "API Gateway is running. Use paths like /v1/license or /v1/person")
	})

	// Gateway가 사용할 포트 설정 (예: 8080)
	port := "8080"
	log.Printf("Starting API Gateway on :%s", port)

	// 웹 서버 시작
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Could not start server: %v", err)
	}
}

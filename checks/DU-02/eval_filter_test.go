package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestEvalFilterTodos(t *testing.T) {
	handler := newAPIHandler(newTestStore(t))
	performRequest[Todo](t, handler, http.MethodPost, "/api/todos", `{"title":"open"}`, http.StatusCreated)
	performRequest[Todo](t, handler, http.MethodPost, "/api/todos", `{"title":"done","completed":true}`, http.StatusCreated)
	complete := performRequest[[]Todo](t, handler, http.MethodGet, "/api/todos?completed=true", "", http.StatusOK)
	if len(complete) != 1 || complete[0].Title != "done" {
		t.Fatalf("completed filter = %+v", complete)
	}
	open := performRequest[[]Todo](t, handler, http.MethodGet, "/api/todos?completed=false", "", http.StatusOK)
	if len(open) != 1 || open[0].Title != "open" {
		t.Fatalf("open filter = %+v", open)
	}
	invalid := httptest.NewRecorder()
	handler.ServeHTTP(invalid, httptest.NewRequest(http.MethodGet, "/api/todos?completed=maybe", nil))
	if invalid.Code != http.StatusBadRequest {
		t.Fatalf("invalid filter status = %d, want 400", invalid.Code)
	}
}

package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestEvalDeleteTodo(t *testing.T) {
	store := newTestStore(t)
	handler := newAPIHandler(store)
	created := performRequest[Todo](t, handler, http.MethodPost, "/api/todos", `{"title":"remove me"}`, http.StatusCreated)
	request := httptest.NewRequest(http.MethodDelete, "/api/todos/1", nil)
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)
	if response.Code != http.StatusNoContent {
		t.Fatalf("DELETE status = %d, want 204; body: %s", response.Code, response.Body.String())
	}
	if _, err := store.Get(created.ID); err != errTodoNotFound {
		t.Fatalf("deleted todo still readable: %v", err)
	}
	missing := httptest.NewRecorder()
	handler.ServeHTTP(missing, request)
	if missing.Code != http.StatusNotFound {
		t.Fatalf("repeat DELETE status = %d, want 404", missing.Code)
	}
}

package api

import (
	"log"
	"net/http"

	"goml/helper"
	"goml/logger"

	"github.com/gorilla/mux"
	tf "github.com/tensorflow/tensorflow/tensorflow/go"
)

type App struct {
	Router  *mux.Router
	Model   *tf.SavedModel
	Handler helper.DataSet
	Meta    helper.DataSet
}

func (a *App) Create(model *tf.SavedModel, handler helper.DataSet, meta helper.DataSet) {
	tracer := logger.GetLogger("api")
	a.Router = mux.NewRouter()
	a.Model = model
	a.Handler = handler
	a.Meta = meta
	tracer.Info("App initalize. (Rest API initalize)")
}

func (a *App) Run(addr string, port string) {
	install(a)
	tracer := logger.GetLogger("api")
	tracer.Info("App Run (%s:%s)", addr, port)
	log.Fatal(http.ListenAndServe(addr+":"+port, a.Router))
}

func (a *App) Route(api string, f func(http.ResponseWriter, *http.Request), method string) {
	a.Router.HandleFunc(api, f).Methods(method)
}

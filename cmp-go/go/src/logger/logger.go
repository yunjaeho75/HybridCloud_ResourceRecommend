package logger

import (
	"fmt"
	"io"
	"log"
	"os"
	"sync"
)

const (
	DEBUG = iota
	INFO
	WARNING
	ERROR
	CRITICAL
)

var locker sync.Mutex

var (
	traceLogger *log.Logger
	infoLogger  *log.Logger
	warnLogger  *log.Logger
	errorLooger *log.Logger
	debugLooger *log.Logger
	fileWriter  io.Writer
	maxLen      int
	logFile     string
	logEntry    map[string]Logger
	logVerbose  int
)

// Logger interface는 Trace, Info, Warn, Error, Debug 형식으로 로그를 출력할 수 있는 함수를 제공한다.
type Logger interface {
	// Trace 는 formating된 문자열에 Prefix으로 Trace 키워드를 붙여 로그를 남긴다.
	Trace(format string, a ...interface{})

	// Info 는 formating된 문자열에 Prefix으로 Info 키워드를 붙여 로그를 남긴다.
	Info(format string, a ...interface{})

	// Warn 는 formating된 문자열에 Prefix으로 Info 키워드를 붙여 로그를 남긴다.
	Warn(format string, a ...interface{})

	// Error 는 formating된 문자열에 Prefix으로 Info 키워드를 붙여 로그를 남긴다.
	Error(format string, a ...interface{})

	// Debug 는 formating된 문자열에 Prefix으로 Info 키워드를 붙여 로그를 남긴다.
	Debug(format string, a ...interface{})
}

// LoggerImp 는 Trace, Info, Warn, Error, Debug 함수를 기능을 제공한다.
type LoggerImp struct {
	name string
}

// New 함수는 LoggerImp를 초기화 해서 새로운 인스턴스를 반환한다.
// 로그는 파일 출력을 기본으로 하고 Standard Output 출력도 같이 한다.
// 설정한 패스에 파일이 생성되지 않으면, Standard Output만 출력한다.
func New(file string) *LoggerImp {

	locker.Lock()
	defer locker.Unlock()

	if fileWriter == nil {
		var fp, err = os.OpenFile(file, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
		if err != nil {
			fileWriter = io.MultiWriter(os.Stdout)
		} else {
			fileWriter = io.MultiWriter(fp, os.Stdout)
		}
	}

	var flags int
	flags = log.Ldate | log.Ltime | log.Lmicroseconds

	if traceLogger == nil {
		//traceLogger = log.New(fileWriter, "TRACE: ", flags)
		traceLogger = log.New(fileWriter, "", flags)
	}

	if infoLogger == nil {
		//infoLogger = log.New(fileWriter, "INFO: ", flags)
		infoLogger = log.New(fileWriter, "", flags)
	}

	if warnLogger == nil {
		//warnLogger = log.New(fileWriter, "WARNING: ", flags)
		warnLogger = log.New(fileWriter, "", flags)
	}

	if errorLooger == nil {
		//errorLooger = log.New(fileWriter, "ERROR: ", flags)
		errorLooger = log.New(fileWriter, "", flags)
	}

	if debugLooger == nil {
		//debugLooger = log.New(fileWriter, "DEBUG: ", flags)
		debugLooger = log.New(fileWriter, "", flags)
	}

	return &LoggerImp{}
}

func SetVerbose(verbose int) {
	logVerbose = verbose
	if verbose < 0 || verbose > 4 {
		logVerbose = INFO
	}
}

func SetLogFile(file string) {
	logFile = file
}

func GetLogFile() string {
	if logFile == "" {
		logFile = "."
	}
	return logFile
}

// GetLogger 함수는 LoggerImp를 초기화 해서 새로운 인스턴스를 반환한다.
func GetLogger(name string) Logger {
	var path string = GetLogFile()

	if logEntry == nil {
		logEntry = make(map[string]Logger)
	}

	logger, err := logEntry[name]
	if !err {
		// fmt.Println("new logger instance.")
		logger := New(path)
		logger.name = name
		logEntry[name] = logger
		return logger
	}

	return logger
}

// Trace 는 formating된 문자열에 Prefix으로 Trace 키워드를 붙여 로그를 남긴다.
func (o *LoggerImp) Trace(format string, a ...interface{}) {
	locker.Lock()
	defer locker.Unlock()
	if logVerbose == DEBUG {
		traceLogger.Printf(o.GetPrefixFormat("TRACE")+o.GetNameFormat()+format, a...)
	}
}

// Debug 는 formating된 문자열에 Prefix으로 Info 키워드를 붙여 로그를 남긴다.
func (o *LoggerImp) Debug(format string, a ...interface{}) {
	locker.Lock()
	defer locker.Unlock()
	if logVerbose == DEBUG {
		debugLooger.Printf(o.GetPrefixFormat("DEBUG")+o.GetNameFormat()+format, a...)
	}
}

// Info 는 formating된 문자열에 Prefix으로 Info 키워드를 붙여 로그를 남긴다.
func (o *LoggerImp) Info(format string, a ...interface{}) {
	locker.Lock()
	defer locker.Unlock()
	if logVerbose <= INFO {
		infoLogger.Printf(o.GetPrefixFormat("INFO")+o.GetNameFormat()+format, a...)
	}
}

// Warn 는 formating된 문자열에 Prefix으로 Info 키워드를 붙여 로그를 남긴다.
func (o *LoggerImp) Warn(format string, a ...interface{}) {
	locker.Lock()
	defer locker.Unlock()
	if logVerbose <= WARNING {
		warnLogger.Printf(o.GetPrefixFormat("WARN")+o.GetNameFormat()+format, a...)
	}
}

// Error 는 formating된 문자열에 Prefix으로 Info 키워드를 붙여 로그를 남긴다.
func (o *LoggerImp) Error(format string, a ...interface{}) {
	locker.Lock()
	defer locker.Unlock()
	// if logVerbose <= ERROR {
	errorLooger.Printf(o.GetPrefixFormat("ERROR")+o.GetNameFormat()+format, a...)
	// }
}

// GetNameFormat 는 로그 이름의 출력 형식을 포멧을 생성하여 반환한다.
// 포멧은 로그 이름 문자열 길이가 최대로 하여 문자열을 오른쪽 정렬하게 한다.
func (o *LoggerImp) GetNameFormat() string {
	maxLen = Max(maxLen, len(o.name))
	nameFormat := fmt.Sprintf("%%-%ds: ", maxLen)
	return fmt.Sprintf(nameFormat, o.name)
}

// GetPrefixFormat 는 로그 Prefix의 출력 형식을 포멧을 생성하여 반환한다.
func (o *LoggerImp) GetPrefixFormat(s string) string {
	return fmt.Sprintf("%-5s ", s)
}

// Max 함수는 정수 x, y 값중 큰 값을 반환한다.
func Max(x, y int) int {
	if x < y {
		return y
	}
	return x
}

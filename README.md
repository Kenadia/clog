# clog

Python logging without shooting yourself in the foot?...

## How to use
- Call `clog.init(OPTIONAL_FILENAME)` from your root module.
- Call `clog.debug()`, `clog.info()`, etc. from the submodules of that module.

## Basic Python logging principles
- Use an application-specific logger instead of the root logger, to avoid affecting the behavior of other modules.
- Use the module hierarchy as the basis for the logger hierarchy.
- Avoid setting a log level on loggers except your top-level logger.

## Controversial Clog logging principles
- Use magic to minimize the code Clog users have to write, at the cost of understandability and performance.
- Provide one way of doing things.

import clog


def main():
  clog.init()
  clog.debug('Hello, world.')
  print(clog.handlers)


if __name__ == '__main__':
  main()

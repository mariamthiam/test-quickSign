import asyncio


def example():
    print("Tâche 'example'")
    print("Lancement de la tâche 'subtask'")
    yield from subtask()
    ensure_future(subtask())   # <- appel à ensure_future au lieu de yield from

    print("Retour dans 'example'")
    for _ in range(3):
        print("(example)")
        yield

def subtask():
    print("Tâche 'subtask'")
    for _ in range(2):
        print("(subtask)")
        yield



DEFAULT_LOOP = Loop()


def ensure_future(coro, loop=None):
    if loop is None:
        loop = DEFAULT_LOOP
    return loop.schedule(coro)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())

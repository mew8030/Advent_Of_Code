from safe import Safe
def main():
    try:
        lock = Safe()
        lock.unlock()
    except Exception as e:
        print(f"ERROR: {e}")

main()

__name__ == "__main__"
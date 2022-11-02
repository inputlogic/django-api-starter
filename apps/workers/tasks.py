from apps.workers import task


@task()
def test(stuff_to_print):
    return stuff_to_print

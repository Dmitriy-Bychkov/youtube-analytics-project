def test_init(sample_string):
    assert isinstance(sample_string.channel_id, str)


def test_print_info(sample_string):
    assert sample_string.print_info() is None
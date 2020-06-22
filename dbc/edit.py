def append_record(record, header, file):
    '''
    file MUST have write permissions
    this method changes the file's position
    '''
    # increment record_count
    header.record_count += 1
    file.seek(0)
    for field in header.to_bytes():
        file.write(field)

    file.seek(header.size + (header.record_count - 1) * header.record_size)
    for field in record.to_bytes():
        file.write(field)
    # write strings...
    file.write(b'\0')


def find(entry, records):
    return next(filter(lambda item: item.entry == entry, records))

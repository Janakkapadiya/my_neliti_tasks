def get_journal_statistics():
    summary = {}
    for the_journal_id in Journal.objects.values_list('id', flat=True):
        journal = Journal.objects.get(id=the_journal_id)
        publications = journal.publication_set.all()
        downloads = 0
        views = 0
        for publication in publications:
            the_hits = publication.hit_set.all()
            for hit in the_hits:
                if hit.action == Hit.DOWNLOAD:
                    downloads += 1
                else:
                    views += 1
        summary[the_journal_id] = (views, downloads)
    return summary

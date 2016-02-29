
import json

mappings = []

categoryDict = {}
categoryDict['categoryCode'] = "PeerReviewed"

dataElements = {}
dataElements['authors'] = 'PeerReviewedAuthors'
dataElements['bookname'] = ''
dataElements['booktitle'] = ''
dataElements['title'] = ''
dataElements['volume'] = 'PeerReviewedJournalVolume'
dataElements['chapter'] = ''
dataElements['edition'] = ''
dataElements['epubdate'] = 'PeerReviewedPublishedDate'
dataElements['fulljournalname'] = 'PeerReviewedJournalTitle'
dataElements['issue'] = 'PeerReviewedJournalIssue'
dataElements['pages'] = 'PeerReviewedPages'
dataElements['uid'] = 'PeerReviewedPMID'
dataElements['publishername'] = ''

categoryDict['dataElements'] = dataElements

mappings.append(categoryDict)

categoryDict = {}
categoryDict['category'] = "NonPeerReviewed"

dataElements = {}
dataElements['authors'] = 'NonPeerReviewedAuthors'
dataElements['bookname'] = ''
dataElements['booktitle'] = ''
dataElements['title'] = ''
dataElements['volume'] = 'NonPeerReviewedJournalVolume'
dataElements['chapter'] = ''
dataElements['edition'] = ''
dataElements['epubdate'] = 'NonPeerReviewedPublishedDate'
dataElements['fulljournalname'] = 'NonPeerReviewedJournalTitle'
dataElements['issue'] = 'NonPeerReviewedJournalIssue'
dataElements['pages'] = 'NonPeerReviewedPages'
dataElements['uid'] = 'NonPeerReviewedPMID'
dataElements['publishername'] = ''

categoryDict['dataElements'] = dataElements

mappings.append(categoryDict)

categoryDict = {}
categoryDict['category'] = "Books"

dataElements = {}
dataElements['authors'] = 'BooksBookAuthors'
dataElements['bookname'] = ''
dataElements['booktitle'] = 'BooksBookTitle'
dataElements['title'] = ''
dataElements['volume'] = 'BooksVolume'
dataElements['chapter'] = 'BooksChapter'
dataElements['edition'] = ''
dataElements['epubdate'] = ''
dataElements['essn'] = ''
dataElements['issn'] = ''
dataElements['fulljournalname'] = ''
dataElements['issue'] = ''
dataElements['pages'] = ''
dataElements['uid'] = ''
dataElements['publishername'] = 'BooksPublisher'

categoryDict['dataElements'] = dataElements

mappings.append(categoryDict)

categoryDict = {}
categoryDict['category'] = "BookChapters"

dataElements = {}
dataElements['authors'] = 'BookChaptersAuthors'
dataElements['bookname'] = ''
dataElements['booktitle'] = ''
dataElements['title'] = 'BookChaptersTitle'
dataElements['volume'] = 'BookChaptersVolume'
dataElements['chapter'] = 'BookChaptersChapter'
dataElements['edition'] = 'BookChaptersEdition'
dataElements['epubdate'] = ''
dataElements['essn'] = ''
dataElements['issn'] = ''
dataElements['fulljournalname'] = ''
dataElements['issue'] = ''
dataElements['pages'] = 'BookChaptersPages'
dataElements['publishername'] = 'BookChaptersPublisher'

categoryDict['dataElements'] = dataElements

mappings.append(categoryDict)

x = json.dumps(mappings)
print x
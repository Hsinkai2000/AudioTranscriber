import React from "react";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch,
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "cv-transcriptions",
});

const config = {
  searchQuery: {
    search_fields: {
      generated_text: { weight: 1 },
    },
    result_fields: {
      generated_text: {
        snippet: {},
      },
      duration: {
        snippet: {},
      },
      age: {
        snippet: {},
      },
      gender: {
        snippet: {},
      },
      accent: {
        snippet: {},
      },
    },
  },
  facets: {
    "age.keyword": { type: "value" },
    "gender.keyword": { type: "value" },
    "accent.keyword": { type: "value" },
    "duration.keyword": { type: "value" },
  },
  autocompleteQuery: {
    results: {
      ResultsPerPage: 5,
      search_fields: {
        generated_text: {
          weight: 3,
        },
      },
      result_fields: {
        generated_text: {
          snippet: {
            size: 100,
            fallback: true,
          },
        },
      },
    },
    suggestions: false,
  },
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true,
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={
                    <SearchBox
                      autocompleteMinimumCharacters={3}
                      autocompleteSuggestions={true}
                      debounceLength={0}
                    />
                  }
                  sideContent={
                    <div>
                      {wasSearched && (
                        <Sorting label={"Sort by"} sortOptions={[]} />
                      )}
                      {Object.keys(config.facets).map((field) => (
                        <Facet
                          key={field}
                          field={field}
                          label={field.replace(".keyword", "")}
                        />
                      ))}
                    </div>
                  }
                  bodyContent={<Results shouldTrackClickThrough={true} />}
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}

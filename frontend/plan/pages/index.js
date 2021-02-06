import React, { useState, useRef, useEffect } from "react";
import Head from "next/head";
import { Provider } from "react-redux";
import { applyMiddleware, createStore } from "redux";
import thunkMiddleware from "redux-thunk";
import SwipeableViews from "react-swipeable-views";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Schedule from "../components/schedule/Schedule";

import {
    initGA,
    logPageView,
    analyticsMiddleware,
} from "../components/analytics";
import coursePlanApp from "../reducers";
import SearchBar from "../components/search/SearchBar";
import Selector from "../components/selector/Selector";
import Footer from "../components/footer";
import Cart from "../components/Cart";
import ModalContainer from "../components/modals/generic_modal_container";
import SearchSortDropdown from "../components/search/SearchSortDropdown";
import Recs from "../components/recomendations/Recs";
import { openModal } from "../actions";
import { preventMultipleTabs } from "../components/syncutils";
import { DISABLE_MULTIPLE_TABS } from "../constants/sync_constants";

let middlewares = [thunkMiddleware, analyticsMiddleware];
if (process.env.NODE_ENV === "development") {
    // eslint-disable-next-line
    const { logger: loggerMiddleware } = require("redux-logger");
    middlewares = [thunkMiddleware, loggerMiddleware, analyticsMiddleware];
}

function Index() {
    const [tab, setTab] = useState(0);
    const [view, setView] = useState(0);
    // FIXME: Hacky, maybe look into redux-persist?
    const [store, setStore] = useState(
        createStore(
            coursePlanApp,
            { schedule: undefined, login: { user: null } },
            applyMiddleware(...middlewares)
        )
    );

    const [storeLoaded, setStoreLoaded] = useState(false);

    // FIXME: Hacky, I'm sure next has some better way to
    // handle this
    const [innerWidth, setInnerWidth] = useState(800);
    const containerRef = useRef();
    const scrollTop = () => window.scrollTo(0, 0);
    const isExpanded = view === 1;

    useEffect(() => {
        setInnerWidth(window.innerWidth);
    }, [setInnerWidth]);

    useEffect(() => {
        logPageView();
    }, []);

    useEffect(() => {
        const previousState = localStorage.getItem("coursePlanSchedules");
        const previousStateJSON = previousState
            ? JSON.parse(previousState)
            : undefined;

        const newStore = createStore(
            coursePlanApp,
            { schedule: previousStateJSON, login: { user: null } },
            applyMiddleware(...middlewares)
        );

        setStore(newStore);
        setStoreLoaded(true);

        newStore.subscribe(() => {
            localStorage.setItem(
                "coursePlanSchedules",
                JSON.stringify(newStore.getState().schedule)
            );
        });
    }, []);

    useEffect(() => {
        if (!localStorage.hasVisited) {
            store.dispatch(
                openModal("WELCOME", {}, "Welcome to Penn Course Plan ✨")
            );
            localStorage.hasVisited = true;
        }

        if (DISABLE_MULTIPLE_TABS) {
            preventMultipleTabs(() => {
                store.dispatch(openModal("MULTITAB", {}, "Multiple tabs"));
            });
        }
    }, [store]);

    const headPreamble = (
        <Head>
            <meta charSet="utf-8" />
            <link
                href="https://fonts.googleapis.com/css?family=Nunito"
                rel="stylesheet"
            />
            <link
                rel="stylesheet"
                href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"
                integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/"
                crossOrigin="anonymous"
            />
            <link rel="shortcut icon" href="/icons/favicon.ico" />
            <link rel="apple-touch-icon-precomposed" sizes="57x57" />
            <link rel="apple-touch-icon-precomposed" sizes="114x114" />
            <link rel="apple-touch-icon-precomposed" sizes="72x72" />
            <link rel="apple-touch-icon-precomposed" sizes="144x144" />
            <link rel="apple-touch-icon-precomposed" sizes="60x60" />
            <link rel="apple-touch-icon-precomposed" sizes="120x120" />
            <link rel="apple-touch-icon-precomposed" sizes="76x76" />
            <link rel="apple-touch-icon-precomposed" sizes="152x152" />
            <link rel="icon" type="image/png" sizes="196x196" />
            <link rel="icon" type="image/png" sizes="96x96" />
            <link rel="icon" type="image/png" sizes="32x32" />
            <link rel="icon" type="image/png" sizes="16x16" />
            <link rel="icon" type="image/png" sizes="128x128" />
            <meta name="application-name" content="&nbsp;" />
            <meta name="msapplication-TileColor" content="#FFFFFF" />
            <meta name="msapplication-TileImage" />
            <meta name="msapplication-square70x70logo" />
            <meta name="msapplication-square150x150logo" />
            <meta name="msapplication-wide310x150logo" />
            <meta name="msapplication-square310x310logo" />

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1, shrink-to-fit=no"
            />
            <meta name="theme-color" content="#000000" />
            <title>Penn Course Plan</title>
        </Head>
    );

    if (innerWidth < 800) {
        return (
            <Provider store={store}>
                {initGA()}
                {headPreamble}
                <SearchBar
                    store={store}
                    setTab={setTab}
                    mobileView
                    storeLoaded={storeLoaded}
                />
                <Tabs value={tab} className="topTabs" centered>
                    <Tab
                        className="topTab"
                        label="Search"
                        onClick={() => setTab(0)}
                    />
                    <Tab
                        className="topTab"
                        label="Cart"
                        onClick={() => setTab(1)}
                    />
                    <Tab
                        className="topTab"
                        label="Schedule"
                        onClick={() => setTab(2)}
                    />
                </Tabs>
                <SwipeableViews
                    index={tab}
                    ref={containerRef}
                    enableMouseEvents
                    onSwitching={scrollTop}
                    onChangeIndex={setTab}
                >
                    <div
                        style={{
                            paddingLeft: "10px",
                            paddingRight: "10px",
                        }}
                    >
                        <div>
                            <div
                                style={{
                                    display: "flex",
                                    flexDirection: "row",
                                    justifyContent: "space-around",
                                    margin: "10px",
                                }}
                            >
                                <SearchSortDropdown />
                            </div>
                            <div
                                className="box"
                                style={{
                                    paddingLeft: 0,
                                    paddingRight: 0,
                                }}
                            >
                                <Selector mobileView view={0} />
                            </div>
                        </div>
                    </div>
                    <div style={{ padding: "10px" }}>
                        <Cart setTab={setTab} mobileView />
                    </div>
                    <div style={{ padding: "10px" }}>
                        <Schedule setTab={setTab} mobileView />
                    </div>
                </SwipeableViews>
                <Footer />
                <ModalContainer />
            </Provider>
        );
    }

    return (
        <Provider store={store}>
            {initGA()}
            {headPreamble}
            <div style={{ padding: "0px 2em 0px 2em" }}>
                <SearchBar
                    storeLoaded={storeLoaded}
                    store={store}
                    setView={setView}
                    style={{ flexGrow: 0 }}
                    isExpanded={isExpanded}
                />
                <div
                    className="App columns is-mobile main smooth-transition"
                    style={
                        isExpanded
                            ? {
                                  padding: 0,
                                  width: "123%",
                              }
                            : {
                                  padding: 0,
                                  width: "129%",
                              }
                    }
                >
                    <div
                        className={
                            isExpanded
                                ? "column smooth-transition is-two-thirds"
                                : "column smooth-transition is-one-fifth"
                        }
                    >
                        <span
                            style={{
                                display: "flex",
                                flexDirection: "row",
                                justifyContent: "space-between",
                            }}
                        >
                            <h3
                                style={{
                                    display: "flex",
                                    fontWeight: "bold",
                                    marginBottom: "0.5rem",
                                }}
                            >
                                Search Results
                            </h3>
                            <div
                                style={{
                                    float: "right",
                                    display: "flex",
                                }}
                            >
                                <SearchSortDropdown />
                            </div>
                        </span>
                        <div
                            className="box"
                            style={{
                                paddingLeft: 0,
                                paddingRight: 0,
                                // display: "flex",
                                // flexDirection: "columnn",
                                // justifyContent: "space-between"
                            }}
                        >
                            <Selector view={view} />
                            
                            <Recs
                                style ={{
                                    bottom: 0
                                }}
                            />
                        </div>
                    </div>
                    <div
                        className="column is-2"
                        style={{
                            display: "flex",
                            flexDirection: "column",
                        }}
                    >
                        <h3
                            style={{
                                display: "flex",
                                fontWeight: "bold",
                                marginBottom: "0.5rem",
                            }}
                        >
                            Cart
                        </h3>
                        <Cart />
                    </div>
                    <div
                        style={{
                            zIndex: 2,
                            paddingRight: "0px",
                            marginRight: "15px",
                        }}
                        className={
                            isExpanded
                                ? "smooth-transition column is-5 hidden"
                                : "smooth-transition column is-5"
                        }
                    >
                        <Schedule />
                    </div>
                </div>
            </div>
            <Footer />
            <ModalContainer />
        </Provider>
    );
}

export default Index;

import "react"
import {SignedIn, SignedOut, UserButton} from "@clerk/clerk-react"
import {Outlet, Link, Navigate} from "react-router-dom"

{/* VID_TIME: 33:11 / 2:31:54 */}
export function Layout() {
        return (
            <div className="app-layout">
                <header className="app-header">
                    <div className="header-content">
                     <h1>MART_BAT Code Challenge Generator </h1>
                     <nav>
                         <SignedIn>
                             <Link to="/">Generate Challenge</Link>
                             <Link to="/history">History</Link>
                             <UserButton/>
                         </SignedIn>
                     </nav>
                    </div>
                </header>

            <main className="app-main">
                <SignedOut>
                    <Navigate to="/sign-in" replace/> {/* replace in current window so that it doesn't change tab*/}
                </SignedOut>
                <SignedIn>
                    <Outlet /> {/* place here whatever was passed to the Layout component*/}
                </SignedIn>
            </main>
        </div>
        );
}
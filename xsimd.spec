#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	tests		# building tests and benchmarks
%bcond_with	xtl		# XTL xcomplex support
#
Summary:	C++ wrappers for SIMD intrinsics
Summary(pl.UTF-8):	Opakowanie C++ dla operacji SIMD
Name:		xsimd
Version:	12.1.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/xtensor-stack/xsimd/tags
Source0:	https://github.com/xtensor-stack/xsimd/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e8887de343bd6036bdfa1f4a4752dc64
Patch0:		%{name}-batch.patch
URL:		https://xsimd.readthedocs.io/
BuildRequires:	cmake >= 3.1
%{?with_tests:BuildRequires:	doctest >= 2.4.9}
BuildRequires:	libstdc++-devel >= 6:4.7
%{?with_xtl:BuildRequires:	libstdc++-devel >= 6:5}
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_xtl:BuildRequires:	xtl-devel >= 0.7.0}
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with tests}
# SSE2 is the lowest supported path
%define		specflags_ia32	-msse2
%endif

%description
SIMD (Single Instruction, Multiple Data) is a feature of
microprocessors that has been available for many years. SIMD
instructions perform a single operation on a batch of values at once,
and thus provide a way to significantly accelerate code execution.
However, these instructions differ between microprocessor vendors and
compilers.

xsimd provides a unified means for using these features for library
authors. Namely, it enables manipulation of batches of numbers with
the same arithmetic operators as for single values. It also provides
accelerated implementation of common mathematical functions operating
on batches.

%description -l pl.UTF-8
SIMD (Single Instruction, Multiple Data - jedna instrukcja, wiele
danych) to funkcjoalność mikroprocesorów dostępna od wielu lat.
Instrukcje SIMD wykonują pojedynczą operację na zbiorze wartości w
jednym czasie, zapewniając mozliwość znaczącego przyspieszenia
wykonywania kodu. Jednak instrukcje te różnią się w zależności od
producenta procesora i kompilatora.

xsimd udostępnia autorom bibliotek ujednolicone sposoby używania tych
funkcji. W szczególności xsimd pozwala operować na zbiorach liczb tymi
samymi operatorami, co na pojedynczych wartościach. Zapewnia także
akcelerowaną implementację popularnych funkcji matematycznych
operujących na zbiorach wartości.

%package devel
Summary:	C++ wrappers for SIMD intrinsics
Summary(pl.UTF-8):	Opakowanie C++ dla operacji SIMD
Group:		Development/Libraries
Requires:	libstdc++-devel >= 6:4.7
%{?with_xtl:Requires:	libstdc++-devel >= 6:5}
%{?with_xtl:Requires:	xtl-devel >= 0.7.0}

%description devel
SIMD (Single Instruction, Multiple Data) is a feature of
microprocessors that has been available for many years. SIMD
instructions perform a single operation on a batch of values at once,
and thus provide a way to significantly accelerate code execution.
However, these instructions differ between microprocessor vendors and
compilers.

xsimd provides a unified means for using these features for library
authors. Namely, it enables manipulation of batches of numbers with
the same arithmetic operators as for single values. It also provides
accelerated implementation of common mathematical functions operating
on batches.

%description devel -l pl.UTF-8
SIMD (Single Instruction, Multiple Data - jedna instrukcja, wiele
danych) to funkcjoalność mikroprocesorów dostępna od wielu lat.
Instrukcje SIMD wykonują pojedynczą operację na zbiorze wartości w
jednym czasie, zapewniając mozliwość znaczącego przyspieszenia
wykonywania kodu. Jednak instrukcje te różnią się w zależności od
producenta procesora i kompilatora.

xsimd udostępnia autorom bibliotek ujednolicone sposoby używania tych
funkcji. W szczególności xsimd pozwala operować na zbiorach liczb tymi
samymi operatorami, co na pojedynczych wartościach. Zapewnia także
akcelerowaną implementację popularnych funkcji matematycznych
operujących na zbiorach wartości.

%package apidocs
Summary:	API documentation for xsimd library
Summary(pl.UTF-8):	Dokumentacja API biblioteki xsimd
Group:		Documentation

%description apidocs
API documentation for xsimd library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki xsimd.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
# fake LIBDIR so we can create noarch package
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_datadir} \
	%{?with_tests:-DBUILD_BENCHMARK=ON} \
	%{?with_tests:-DBUILD_TESTS=ON}

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE README.md
%{_includedir}/xsimd
%{_npkgconfigdir}/xsimd.pc
%{_datadir}/cmake/xsimd

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_images,_static,api,*.html,*.js}
%endif

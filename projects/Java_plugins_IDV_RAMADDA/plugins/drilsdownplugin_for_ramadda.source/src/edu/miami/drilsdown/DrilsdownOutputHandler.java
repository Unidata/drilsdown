/*
 * Copyright (c) 2008-2016 Geode Systems LLC
 * This Software is licensed under the Geode Systems RAMADDA License available in the source distribution in the file 
 * ramadda_license.txt. The above copyright notice shall be included in all copies or substantial portions of the Software.
 */

package edu.miami.drilsdown;


import org.ramadda.repository.Entry;
import org.ramadda.repository.Link;
import org.ramadda.repository.Repository;
import org.ramadda.repository.RepositoryUtil;
import org.ramadda.repository.Request;
import org.ramadda.repository.Result;
import org.ramadda.repository.map.*;
import org.ramadda.repository.metadata.ContentMetadataHandler;
import org.ramadda.repository.metadata.Metadata;
import org.ramadda.repository.output.OutputHandler;
import org.ramadda.repository.output.OutputType;


import org.ramadda.repository.type.TypeHandler;
import org.ramadda.util.HtmlUtils;
import org.ramadda.util.Json;
import org.ramadda.util.SelectionRectangle;
import org.ramadda.util.Utils;

import org.w3c.dom.Element;

import ucar.unidata.util.IOUtil;



import java.io.File;

import java.util.ArrayList;
import java.util.List;


/**
This class supports generating IDV ISL files for IDV bundle entries
 */
public class DrilsdownOutputHandler extends OutputHandler {

    public static final String ARG_MAKENOTEBOOK = "makenotebook";



    /** The OutputType definition for the generated ISL */
    public static final OutputType OUTPUT_ISL =
        new OutputType("Geolocated IDV ISL", "idv.isl",
                       OutputType.TYPE_OTHER, "", "/idv/idv.gif");


    /** The OutputType definition for the end-user ISL form */
    public static final OutputType OUTPUT_ISLFORM =
        new OutputType("Geolocated IDV ISL Form", "idv.islform",
                       OutputType.TYPE_OTHER, "", "/idv/idv.gif");


    /** The OutputType definition for the generated notebooks for folders */
    public static final OutputType OUTPUT_NOTEBOOK =
        new OutputType("iPython Notebook", "drilsdown.notebook",
                       OutputType.TYPE_OTHER, "", "/icons/python.png");




    /**
     * CTOR
     *
     * @param repository  the repository
     * @param element     the Entry to serve
     * @throws Exception  problem creating handler
     */
    public DrilsdownOutputHandler(Repository repository, Element element)
            throws Exception {
        super(repository, element);
        addType(OUTPUT_ISL);
        addType(OUTPUT_ISLFORM);
        addType(OUTPUT_NOTEBOOK);
    }



    /**
     * Get the entry links if the entry is an IDV bundle file
     *
     * @param request  the Request
     * @param state    the Entry
     * @param links    the list of links to add to
     *
     * @throws Exception  problems
     */
    public void getEntryLinks(Request request, State state, List<Link> links)
            throws Exception {

        Entry entry = state.getEntry();
        if (entry == null) {
            return;
        }
        if(entry.isGroup()) {
            String suffix   = "/" + IOUtil.stripExtension(entry.getName()) + ".ipynb";
            links.add(makeLink(request, state.getEntry(), OUTPUT_NOTEBOOK,suffix));
        }

        if (entry.getResource().getPath().endsWith(".xidv")
                || entry.getResource().getPath().endsWith(".zidv")) {
            String fileTail = getStorageManager().getFileTail(entry);
            String suffix   = "/" + IOUtil.stripExtension(fileTail) + ".isl";
            //                suffix = java.net.URLEncoder.encode(suffix);
            links.add(makeLink(request, state.getEntry(), OUTPUT_ISLFORM,
                               suffix));
            links.add(makeLink(request, state.getEntry(), OUTPUT_ISL,
                               suffix));
        }
    }


    /**
     * Output a group
     *
     * @param request     the Request
     * @param outputType  the OutputType
     * @param group       the group to output
     * @param subGroups   subgroups
     * @param entries     list of Entrys
     *
     * @return  the Result
     *
     * @throws Exception  problems
     */
    public Result outputGroup(Request request, OutputType outputType,
                              Entry group, List<Entry> subGroups,
                              List<Entry> entries)
            throws Exception {
        if(outputType.equals(OUTPUT_NOTEBOOK)) {
            return outputGroupNotebook(request, group, subGroups, entries);
        }
        return outputEntry(request, outputType, group);
    }


    public Result outputGroupNotebook(Request request, 
                              Entry group, List<Entry> subGroups,
                              List<Entry> entries)
            throws Exception {
        List<String> mainMap = new ArrayList<String>();
        List<String> codeCells  = new ArrayList<String>();
        List<String> codeLines = new ArrayList<String>();
        codeLines.add("#Code generated from RAMADDA\n");
        codeLines.add("global generatedNotebook;\n");
        codeLines.add("generatedNotebook = True;\n");
        codeLines.add("%reload_ext drilsdown\n");
        codeLines.add("from drilsdown import Ramadda;\n");
        codeLines.add("from drilsdown import RamaddaEntry;\n");
        codeLines.add("from drilsdown import Idv;\n");
        codeLines.add("from drilsdown import DrilsdownUI;\n");
        codeLines.add("entries=[];\n");
        subGroups.addAll(entries);
        codeLines.add("theRamadda = Ramadda('" + request.getAbsoluteUrl(getRepository().URL_ENTRY_SHOW)+"?entryid=" + group.getId() +  "');\n");

        for(Entry entry: subGroups) {
            
            String icon = getPageHandler().getIconUrl(request, entry);
            String url = "";
            String fileSize = "0";
            codeLines.add("entries.add(RamaddaEntry(theRamadda, '" + entry.getName()+"', '" + entry.getId() +"' , '" + entry.getType() +"' , '" + icon+"' , '" + url +"', " + fileSize+"));\n");
        }
        codeLines.add("theRamadda.displayEntries('Entries', entries);\n");

        codeCells.add(makeCodeCell(codeLines));
        codeLines = new ArrayList<String>();


        //        codeLines.add("Idv.loadBundle(bundleUrl);\n");
        //        codeLines.add("Idv.makeImage(False,\"" +  entry.getName().replaceAll(" ","-") +"\");\n");

        codeCells.add(makeCodeCell(codeLines));
        mainMap.add("cells");
        mainMap.add(Json.list(codeCells));


        mainMap.add("metadata");
        String bulkMetadata = getRepository().getResource("/edu/miami/drilsdown/metadata.json");
        mainMap.add(bulkMetadata);
        mainMap.add("nbformat");
        mainMap.add("4");
        mainMap.add("nbformat_minor");
        mainMap.add("0");


        StringBuilder notebook = new StringBuilder(Json.map(mainMap));
        Result result = new Result("", notebook, "application/x-ipynb+json");
        result.setReturnFilename(group.getName() + ".ipynb");
        return result;
    }



    /**
     * Make the ISL form
     *
     * @param request The request
     * @param outputType The output
     * @param entry The entry
     *
     * @return The ISL form result
     *
     * @throws Exception On  badness
     */
    public Result outputEntryForm(Request request, OutputType outputType,
                                  Entry entry)
            throws Exception {
        if (request.exists(ARG_SUBMIT)) {
            return outputEntryIsl(request, outputType, entry);
        }
        if(request.exists(ARG_MAKENOTEBOOK)) {
            return outputEntryNotebook(request, outputType, entry);
        }

        StringBuilder sb = new StringBuilder();
        getPageHandler().entrySectionOpen(request, entry, sb, "IDV ISL Form");
        String formUrl = request.makeUrl(getRepository().URL_ENTRY_SHOW);
        String formId  = HtmlUtils.getUniqueId("form_");
        sb.append(HtmlUtils.form(formUrl, HtmlUtils.id(formId)));
        sb.append(HtmlUtils.hidden(ARG_ENTRYID, entry.getId()));
        sb.append(HtmlUtils.hidden(ARG_OUTPUT, OUTPUT_ISLFORM.toString()));
        sb.append(HtmlUtils.formTable());
        SelectionRectangle bbox = TypeHandler.getSelectionBounds(request);
        MapInfo map = getRepository().getMapManager().createMap(request,
                          true, null);

        String mapSelector = map.makeSelector("bounds", true,
                                 bbox.getStringArray(), "", "");
        sb.append(formEntry(request, msgLabel("Area"), mapSelector));

        String fromDate = getPageHandler().makeDateInput(request,
                              ARG_FROMDATE, formId, null, null, false);
        String endDate = getPageHandler().makeDateInput(request, ARG_TODATE,
                             formId, null, null, false);

        sb.append(formEntry(request, msgLabel("Date Range"),
                            "From: " + fromDate + "  To: " + endDate
                            ));
        sb.append(HtmlUtils.submit(msg("Make ISL"), ARG_SUBMIT));
        sb.append(HtmlUtils.space(2));
        sb.append(HtmlUtils.submit(msg("Make IPython Notebook"), ARG_MAKENOTEBOOK));
        sb.append(HtmlUtils.formTableClose());

        sb.append(HtmlUtils.formClose());

        sb.append("<p>");
        sb.append("To make a URL directly do:<br>");
        String example = request.getAbsoluteUrl(formUrl) + "?" + ARG_ENTRYID
                         + "=" + entry.getId() + "&" + ARG_OUTPUT + "="
                         + OUTPUT_ISL.toString()
                         + "&north=90&west=-180&south=-90&east=180" + "&"
                         + ARG_FROMDATE + "=2015-01-01" + "&" + ARG_TODATE
                         + "=2016-01-01";
        sb.append(HtmlUtils.href(example, example));
        getPageHandler().entrySectionClose(request, entry, sb);

        Result result = new Result("", sb);

        return result;
    }


    /**
     * Output an Entry. This either handles the ISL generation or the ISL form request
     *
     * @param request     the Request
     * @param outputType  type of Output
     * @param entry       the Entry
     *
     * @return  the Result
     *
     * @throws Exception problems
     */
    public Result outputEntry(Request request, OutputType outputType,
                              Entry entry)
            throws Exception {
        if (outputType.equals(OUTPUT_ISLFORM)) {
            return outputEntryForm(request, outputType, entry);
        }

        return outputEntryIsl(request, outputType, entry);
    }

    /**
     * Generate the IDV ISL file
     *
     * @param request The request
     * @param outputType The output type
     * @param entry The entry
     *
     * @return the result ISL
     *
     * @throws Exception on badness
     */
    public Result outputEntryIsl(Request request, OutputType outputType,
                                 Entry entry)
            throws Exception {


        StringBuilder isl      = new StringBuilder();


        String        fileTail = getStorageManager().getFileTail(entry);
        String url =
            HtmlUtils.url(request.makeUrl(getRepository().URL_ENTRY_GET)
                          + "/" + fileTail, ARG_ENTRYID, entry.getId());
        url = request.getAbsoluteUrl(url);
        isl.append("<isl>\n<bundle file=\"");
        isl.append(url);
        isl.append("\" ");


        //Get the bounds from the arguments
        //Support both north= and bounds_north=
        String north = request.getString("north",
                                         request.getString("bounds_north",
                                             "90"));
        String west = request.getString("west",
                                        request.getString("bounds_west",
                                            "-180"));
        String south = request.getString("south",
                                         request.getString("bounds_south",
                                             "-90"));
        String east = request.getString("east",
                                        request.getString("bounds_east",
                                            "180"));
        boolean haveBbox =
            Utils.stringDefined(north)
            && (Utils.stringDefined(west) & Utils.stringDefined(south))
            && Utils.stringDefined(east);
        if (haveBbox) {
            isl.append(" bbox=\"" + north + "," + west + "," + south + ","
                       + east + "\"");
        }

        //Get the date ranges
        String fromDate = request.getString(ARG_FROMDATE, (String) null);
        String toDate   = request.getString(ARG_TODATE, (String) null);
        if (Utils.stringDefined(fromDate)) {
            isl.append(" timedriverstart=\"" + fromDate + " 00:00:00\"");
        }
        if (Utils.stringDefined(toDate)) {
            isl.append(" timedriverend=\"" + toDate + " 24:00:00\"");
        }


        isl.append("/>\n");
        isl.append("<pause/>\n");
        if (haveBbox) {
            isl.append("<center useprojection=\"true\" north=\"" + north + "\" west=\"" + west
                       + "\" south=\"" + south + "\" east=\"" + east
                       + "\" />\n");
        }
        isl.append("</isl>\n");
        Result result = new Result("", isl, "application/x-idv-isl");
        result.setReturnFilename(fileTail + ".isl");

        return result;
    }
    private String makeCodeCell(List<String> codeLines) {
        List<String> codeCell = new ArrayList<String>();
        codeCell.add("cell_type");
        codeCell.add(Json.quote("code"));
        codeCell.add("execution_count");
        codeCell.add("1");
        codeCell.add("metadata");
        codeCell.add(Json.map("collapsed","false"));
        codeCell.add("outputs");
        codeCell.add(Json.list());
        codeCell.add("source");
        codeCell.add(Json.list(codeLines,true));
        return Json.map(codeCell);
    }

    public Result outputEntryNotebook(Request request, OutputType outputType,
                                 Entry entry)
            throws Exception {

        List<String> mainMap = new ArrayList<String>();
        String        fileTail = getStorageManager().getFileTail(entry);
        String url =
            HtmlUtils.url(request.makeUrl(getRepository().URL_ENTRY_GET)
                          + "/" + fileTail, ARG_ENTRYID, entry.getId());
        url = request.getAbsoluteUrl(url);
        Entry parentEntry  = entry.getParentEntry();

        List<String> codeCells  = new ArrayList<String>();
        List<String> codeLines = new ArrayList<String>();
        codeLines.add("#Code generated from RAMADDA\n");
        codeLines.add("#uncomment if you have drilsdown installed as an extension\n");
        codeLines.add("#%reload_ext drilsdown\n");
        codeLines.add("from drilsdown import Repository;\n");
        codeLines.add("from drilsdown import Ramadda;\n");
        codeLines.add("from drilsdown import Idv;\n");

        codeLines.add("Repository.set_repository(Ramadda(\"" + request.getAbsoluteUrl(getRepository().getUrlBase()+"/entry/show") + "?" + ARG_ENTRYID
                      + "=" + parentEntry.getId()+"\"),False);\n");
        codeCells.add(makeCodeCell(codeLines));
        codeLines = new ArrayList<String>();
        codeLines.add("bundleUrl = \"" +  url +"\"" +"\n");
        codeLines.add("bundleName = \"" +  entry.getName() +"\"" +"\n");

        //Get the bounds from the arguments
        //Support both north= and bounds_north=
        String north = request.getString("north",
                                         request.getString("bounds_north",
                                             "90"));
        String west = request.getString("west",
                                        request.getString("bounds_west",
                                            "-180"));
        String south = request.getString("south",
                                         request.getString("bounds_south",
                                             "-90"));
        String east = request.getString("east",
                                        request.getString("bounds_east",
                                            "180"));
        boolean haveBbox =
            Utils.stringDefined(north)
            && (Utils.stringDefined(west) & Utils.stringDefined(south))
            && Utils.stringDefined(east);
        if (haveBbox) {
            //            isl.append(" bbox=\"" + north + "," + west + "," + south + ","
            //                       + east + "\"");
        }


        //Get the date ranges
        String fromDate = request.getString(ARG_FROMDATE, (String) null);
        String toDate   = request.getString(ARG_TODATE, (String) null);
        if (Utils.stringDefined(fromDate)) {
            //            isl.append(" timedriverstart=\"" + fromDate + "\"");
        }
        if (Utils.stringDefined(toDate)) {
            //            isl.append(" timedriverend=\"" + toDate + "\"");
        }

        if (haveBbox) {
            codeLines.add("%setBBOX  " +  north + " " +  west + " " + south + " "  + east +"\n");
        }

        codeLines.add("Idv.load_bundle(bundleUrl);\n");
        codeLines.add("Idv.make_image(publish=False, caption=\"" +  entry.getName().replaceAll(" ","-") +"\");\n");

        codeCells.add(makeCodeCell(codeLines));
        mainMap.add("cells");
        mainMap.add(Json.list(codeCells));


        mainMap.add("metadata");
        String bulkMetadata = getRepository().getResource("/edu/miami/drilsdown/metadata.json");
        mainMap.add(bulkMetadata);
        mainMap.add("nbformat");
        mainMap.add("4");
        mainMap.add("nbformat_minor");
        mainMap.add("0");



        StringBuilder notebook = new StringBuilder(Json.map(mainMap));
        Result result = new Result("", notebook, "application/x-ipynb+json");
        result.setReturnFilename(fileTail + ".ipynb");

        return result;
    }






}
